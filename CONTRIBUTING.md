# Contributing to Trip Ethiopia Bot

Thank you for considering contributing to Trip Ethiopia Bot! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, etc.)

### Suggesting Features

We welcome feature suggestions! Please create an issue with:
- Clear description of the feature
- Use case and benefits
- Potential implementation approach (optional)

### Code Contributions

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/trip-ethiopia-bot.git
   cd trip-ethiopia-bot
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed
   - Add tests if applicable

4. **Test Your Changes**
   ```bash
   pytest tests/
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Describe your changes
   - Submit the PR

## 📝 Code Style Guidelines

### Python Style
- Follow PEP 8 style guide
- Use type hints where possible
- Maximum line length: 100 characters
- Use descriptive variable names

### Example:
```python
def calculate_total_price(
    base_price: float,
    tax_rate: float,
    discount: float = 0.0
) -> float:
    """
    Calculate total price with tax and discount.
    
    Args:
        base_price: Base price before tax
        tax_rate: Tax rate as decimal (e.g., 0.15 for 15%)
        discount: Discount amount
    
    Returns:
        Total price after tax and discount
    """
    taxed_price = base_price * (1 + tax_rate)
    final_price = taxed_price - discount
    return round(final_price, 2)
```

### Commit Messages
Use clear, descriptive commit messages:
- `Add: description` - New feature
- `Fix: description` - Bug fix
- `Update: description` - Update existing feature
- `Refactor: description` - Code refactoring
- `Docs: description` - Documentation changes
- `Test: description` - Test changes

## 🏗️ Project Structure

```
trip/
├── bot/              # Bot handlers and keyboards
├── config/           # Configuration and settings
├── models/           # Database models
├── services/         # External API integrations
├── tasks/            # Background tasks
├── utils/            # Utility functions
├── locales/          # Translation files
├── tests/            # Unit and integration tests
└── main.py           # Application entry point
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_handlers.py
```

### Writing Tests
```python
import pytest
from bot.handlers import start_command

@pytest.mark.asyncio
async def test_start_command():
    """Test /start command."""
    # Your test implementation
    pass
```

## 📖 Documentation

### Adding New Features
When adding new features:
1. Update README.md if it affects usage
2. Add docstrings to functions/classes
3. Update API documentation if applicable
4. Add examples if needed

### Translation
To add a new language:
1. Create `locales/xx.json` (where xx is language code)
2. Copy structure from `locales/en.json`
3. Translate all strings
4. Add language code to `config/settings.py`

## 🔐 Security

### Reporting Security Issues
**Do not create public issues for security vulnerabilities.**

Instead, email: security@tripethiopia.com

### Security Best Practices
- Never commit API keys or secrets
- Use environment variables for sensitive data
- Validate all user inputs
- Sanitize data before database operations

## 🌍 Internationalization

### Adding Translations
1. Add new keys to all locale files
2. Use descriptive key names
3. Test with different languages
4. Consider text length variations

### Example:
```json
{
  "errors": {
    "invalid_date": "❌ Invalid date format. Please use YYYY-MM-DD."
  }
}
```

## 📋 Pull Request Checklist

Before submitting a PR, ensure:
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added (if applicable)
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] PR description is detailed

## 📞 Getting Help

If you need help:
- Check existing documentation
- Search existing issues
- Create a new issue with [Question] tag
- Join our community chat (if available)

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Thank you for contributing to Trip Ethiopia Bot! Your efforts help make travel easier for Ethiopian travelers.

---

**Made with ❤️ for Ethiopia 🇪🇹**


