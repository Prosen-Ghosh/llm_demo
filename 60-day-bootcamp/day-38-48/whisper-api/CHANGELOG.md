# Changelog

## Recent Changes

*   **`Dockerfile`**:
    *   Added `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, and `CT_NUM_THREADS` environment variables to control the number of threads for performance optimization.

*   **`Makefile`**:
    *   Added a new `test-file` target to run specific test files.

*   **`requirements.txt`**:
    *   Added `psutil` for system monitoring.
    *   Added `pytest-asyncio` for testing asynchronous code.

*   **`app/main.py`**:
    *   Added system health monitoring and periodic garbage collection.
    *   Implemented different processing modes (`ACCURATE`, `BALANCED`, `TURBO`) for transcription, which control `beam_size` and `best_of` parameters.
    *   Added support for providing custom keywords to the transcription process as an `initial_prompt`.
    *   Added a `/stream` endpoint for real-time transcription streaming.
    *   Language detection is now automatic by default (`language="auto"`).

*   **`app/whisper.py`**:
    *   The `transcribe_file` method now accepts more parameters for fine-tuning the transcription process (`beam_size`, `best_of`, `patience`, `initial_prompt`).
    *   Added `stream_transcribe` method to support the new streaming endpoint.
    - The transcription result now includes more metadata, like `inference_time` and `real_time_factor`.

*   **`app/worker.py`**:
    *   The `process_transcription_job` now accepts and passes the new transcription parameters (`beam_size`, `best_of`, `initial_prompt`) to `whisper_service.transcribe_file`.
    *   Caching of transcription results is implemented using a file hash.

*   **`Dockerfile`**:
    *   Added `ffmpeg` to the Docker image.

*   **`app/config.py`**:
    *   Renamed `WHISPER_MODEL_SIZE` to `DEFAULT_MODEL_SIZE`.
    *   Added `ALLOWED_MODELS` to specify a list of allowed models.
    *   Increased `CPU_THREADS` to 2.
    *   Added `NUMBER_OF_WORKERS` with a value of 4.

*   **`app/main.py`**:
    *   Added `Query` to the imports.
    *   Imported `check_model_suitability` and `normalize_audio`.
    *   The `/` endpoint now returns the `DEFAULT_MODEL_SIZE` instead of `WHISPER_MODEL_SIZE`.
    *   The `/transcribe` endpoint now accepts a `language` parameter.
    *   The `/transcribe` endpoint now normalizes the audio before transcription.
    *   The `/transcribe` endpoint now checks for model suitability based on the language.
    *   The `/transcribe` endpoint now includes more information in the response, such as `model_used`, `language_probability`, and an optional `system_warning`.
    *   The `/transcribe` endpoint now deletes the processed file after transcription.
    *   Removed the `/test-transcribe` endpoint.
    *   Added a new `/system/model` endpoint to switch the model at runtime.

*   **`app/utils.py`**:
    *   Added `.ogg` to the list of `SUPPORTED_EXTENSIONS`.
    *   Added `LANGUAGE_MODEL_REQUIREMENTS` to define recommended models for different languages.
    *   Added `check_model_suitability` function to check if the current model is suitable for the given language.

*   **`app/whisper.py`**:
    *   Imported `gc`.
    *   The `load_model` method now accepts a `model_size` parameter to switch models.
    *   The `load_model` method now unloads the previous model before loading a new one.
    *   The `transcribe_file` method now accepts a `language` parameter.
    *   The `transcribe_file` method now uses more advanced transcription options like `beam_size`, `best_of`, `temperature`, `vad_filter`, and `patience`.
    *   The `transcribe_file` method now returns the `model_used` in the result.

*   **`requirements.txt`**:
    *   Added `ffmpeg-python`.
