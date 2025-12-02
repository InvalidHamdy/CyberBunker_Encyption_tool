

```markdown
# CyberBunker

A Python/Tkinter desktop application that demonstrates multiple classical and modern cryptographic algorithms with a GUI. The app includes user authentication, password recovery, and file-based encryption/decryption workflows.

## Features
- GUI built with `tkinter` and `customtkinter`
- Implementations of common ciphers:
  - Caesar (`algorithms/CeaserCipher.py`)
  - Affine (`algorithms/AFFINE.py`)
  - Vigenère, Playfair, Rail Fence, ROT13, Substitution, RSA (see `algorithms/` folder)
- User authentication and password recovery handlers in `services/`
- Simple file upload / overwrite support in the encryption UI
- RSA key generation and encryption helpers
- Test file for Caesar cipher: `test.py`

## Repo structure
- `app.py` — application entry point
- `LogIn.py` — login UI and navigation
- `AlgorithmDashBoard.py` — dashboard UI for algorithm selection
- `EncryptionPage.py` — main encryption/decryption UI
- `algorithms/` — cipher implementations and utilities
- `services/` — business logic (login, forgot password, OTP, etc.)
- `database/DATABASE_CYBERSECURTY.sql` — sample SQL for initial DB (editable)
- `test.py` — simple unit test for Caesar cipher
- `background3.png`, `Frame 1.png`, `logo.png` — UI assets

## Requirements
- Python 3.8+
- Recommended packages (put into `requirements.txt`):
  - `pillow`
  - `customtkinter`
  - `python-dotenv`
  - `sqlitecloud`
  - (add any other algorithms' dependencies)

Install dependencies:
```bash
python -m pip install -r requirements.txt
```

## Configuration
Create a `.env` file in the project root with at least:
```
CONNECTION_STRING=<your_sqlitecloud_connection_string_or_db_path>
```
Adjust the connection string to match your `sqlitecloud` configuration or local SQLite DB.

## Database
A sample SQL file is provided at `database/DATABASE_CYBERSECURTY.sql`. Review and correct column names or data as needed before seeding the database.

## Running the app
From project root:
```bash
python app.py
```
This launches the login window. Use the UI to navigate to the dashboard and encryption pages.

## Tests
Run the simple Caesar cipher test:
```bash
python test.py
```

## Notes and development tips
- UI depends on local image assets (`background3.png`, `Frame 1.png`, `logo.png`) — ensure these exist in the working directory.
- Environment and DB connection must be configured before attempting login or password reset flows.
- Handlers in `services/` use `sqlitecloud` and `python-dotenv`—verify credentials and environment variables.

## Contributing
- Fork, create a feature branch, and submit a pull request.
- Add unit tests for new cipher implementations or bug fixes.

## License
No license specified. Add a `LICENSE` file to clarify terms.
```
