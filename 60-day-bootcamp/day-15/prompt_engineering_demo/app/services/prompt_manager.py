from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime

from app.models.prompts import Base, PromptVersionDB
from app.models.schemas import PromptVersion, PromptStrategy


class PromptVersionManager:
    """Manages prompt versioning with SQLite backend"""
    
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=False)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
    
    async def initialize(self):
        """Create tables and seed default prompts"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # Seed default prompts
        await self._seed_defaults()
    
    async def _seed_defaults(self):
        """Seed default prompt versions"""
        defaults = [
            PromptVersion(
                version="v1.0.0",
                name="Base CoT Prompt",
                system_prompt="You are a helpful AI assistant with expertise in reasoning and problem-solving.",
                strategy=PromptStrategy.CHAIN_OF_THOUGHT
            ),
            PromptVersion(
                version="v1.0.0",
                name="Base ReAct Prompt",
                system_prompt="You are an AI assistant that breaks down complex queries into actionable steps.",
                strategy=PromptStrategy.REACT
            )
        ]
        
        for prompt in defaults:
            existing = await self.get_version(prompt.version, prompt.strategy.value)
            if not existing:
                await self.create_version(prompt)
    
    async def create_version(self, prompt: PromptVersion) -> PromptVersion:
        """Create a new prompt version"""
        async with self.async_session() as session:
            db_prompt = PromptVersionDB(
                version=prompt.version,
                name=prompt.name,
                system_prompt=prompt.system_prompt,
                strategy=prompt.strategy.value,
                created_by=prompt.created_by,
                changelog=prompt.changelog,
                is_active=prompt.is_active,
                performance_metrics=prompt.performance_metrics
            )
            session.add(db_prompt)
            await session.commit()
            return prompt
    
    async def get_version(
        self, 
        version: str, 
        strategy: str
    ) -> Optional[PromptVersion]:
        """Retrieve a specific prompt version"""
        async with self.async_session() as session:
            result = await session.execute(
                select(PromptVersionDB).where(
                    PromptVersionDB.version == version,
                    PromptVersionDB.strategy == strategy
                )
            )
            
            db_prompt = result.scalar_one_or_none()
            print(f"result=> {version} :: strategy => {strategy}")
            if db_prompt:
                return PromptVersion(
                    version=db_prompt.version,
                    name=db_prompt.name,
                    system_prompt=db_prompt.system_prompt,
                    strategy=PromptStrategy(db_prompt.strategy),
                    created_at=db_prompt.created_at,
                    created_by=db_prompt.created_by,
                    changelog=db_prompt.changelog,
                    is_active=db_prompt.is_active,
                    performance_metrics=db_prompt.performance_metrics
                )
            return None
    
    async def list_versions(self, strategy: Optional[str] = None) -> List[PromptVersion]:
        """List all prompt versions, optionally filtered by strategy"""
        async with self.async_session() as session:
            query = select(PromptVersionDB)
            if strategy:
                query = query.where(PromptVersionDB.strategy == strategy)
            
            result = await session.execute(query.order_by(PromptVersionDB.created_at.desc()))
            db_prompts = result.scalars().all()
            
            return [
                PromptVersion(
                    version=p.version,
                    name=p.name,
                    system_prompt=p.system_prompt,
                    strategy=PromptStrategy(p.strategy),
                    created_at=p.created_at,
                    created_by=p.created_by,
                    changelog=p.changelog,
                    is_active=p.is_active,
                    performance_metrics=p.performance_metrics
                )
                for p in db_prompts
            ]
    
    async def update_metrics(
        self, 
        version: str, 
        strategy: str, 
        metrics: dict
    ):
        """Update performance metrics for a prompt version"""
        async with self.async_session() as session:
            result = await session.execute(
                select(PromptVersionDB).where(
                    PromptVersionDB.version == version,
                    PromptVersionDB.strategy == strategy
                )
            )
            db_prompt = result.scalar_one_or_none()
            if db_prompt:
                db_prompt.performance_metrics = metrics
                await session.commit()