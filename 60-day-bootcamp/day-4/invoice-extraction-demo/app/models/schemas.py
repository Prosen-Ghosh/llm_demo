from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Annotated, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"

class InvoiceLineItem(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    description: Annotated[str, Field(min_length=1,  max_length=500, description="Product or service description")]
    quantity: Annotated[Decimal, Field(gt=0, description="Quantity of items")]
    unit_price: Annotated[Decimal, Field( ge=0, description="Price per unit")]
    line_total: Annotated[Decimal, Field(ge=0, description="Total for this line (quantity * unit_price)")]
    
    @field_validator('line_total')
    @classmethod
    def validate_line_total(cls, v: Decimal, info) -> Decimal:
        if info.data.get('quantity') and info.data.get('unit_price'):
            expected = info.data['quantity'] * info.data['unit_price']
            # Allow for small rounding differences
            if abs(v - expected) > Decimal('0.01'):
                raise ValueError(f"Line total {v} doesn't match quantity * unit_price = {expected}")
        return v

class VendorInfo(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    name: Annotated[str, Field(min_length=1, max_length=200, description="Vendor company name")]
    address: Optional[str] = Field(None, max_length=500)
    tax_id: Optional[str] = Field(None, max_length=50, description="VAT/Tax ID")
    contact_email: Optional[str] = Field(None, max_length=100)

class InvoiceData(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    invoice_number: Annotated[str, Field(min_length=1, max_length=100, description="Unique invoice identifier")]
    invoice_date: Annotated[date, Field(description="Date invoice was issued")]
    due_date: Optional[date] = Field(None, description="Payment due date")
    
    vendor: VendorInfo
    
    line_items: Annotated[list[InvoiceLineItem], Field(min_length=1, description="List of invoice line items")]
    
    subtotal: Annotated[Decimal, Field(ge=0, description="Sum of all line items")]
    tax_amount: Annotated[Decimal, Field(ge=0, description="Total tax amount")]
    total_amount: Annotated[Decimal, Field(gt=0, description="Final amount due (subtotal + tax)")]
    
    currency: Currency = Field(default=Currency.USD)
    notes: Optional[str] = Field(None, max_length=1000)
    
    @field_validator('total_amount')
    @classmethod
    def validate_total(cls, v: Decimal, info) -> Decimal:
        if info.data.get('subtotal') is not None and info.data.get('tax_amount') is not None:
            expected = info.data['subtotal'] + info.data['tax_amount']
            if abs(v - expected) > Decimal('0.01'):
                raise ValueError(f"Total {v} doesn't match subtotal + tax = {expected}")
        return v


class ExtractionResult(BaseModel):
    success: bool
    data: Optional[InvoiceData] = None
    errors: list[str] = Field(default_factory=list)
    confidence_score: Annotated[float, Field(ge=0.0, le=1.0)] = 1.0
    strategy_used: str  # "ollama_json", "openrouter_function", "repair"
    retry_count: int = 0
    partial_data: Optional[dict] = None  # If validation failed, store what we got


class ExtractionRequest(BaseModel):
    invoice_text: Annotated[str, Field(min_length=10, max_length=50000, description="Raw text content of the invoice")]
    prefer_strategy: Optional[str] = Field(None, description="Force a specific strategy: 'ollama', 'openrouter', or 'auto'")