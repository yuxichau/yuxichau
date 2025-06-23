# My Static Website

This is a simple static website project that is hosted on GitHub Pages. The project includes HTML, CSS, and JavaScript files, along with a favicon.

## Project Structure

```
my-static-website
├── src
│   ├── index.html        # Main HTML document
│   ├── css
│   │   └── styles.css    # Styles for the website
│   ├── js
│   │   └── main.js       # JavaScript functionality
│   └── assets
│       └── favicon.ico    # Favicon for the website
├── .github
│   └── workflows
│       └── deploy.yml     # GitHub Actions workflow for deployment
├── .gitignore             # Files to ignore by Git
└── README.md              # Project documentation
```

## Setup Instructions

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/yourusername/my-static-website.git
   ```

2. Navigate to the project directory:
   ```
   cd my-static-website
   ```

3. Open the `src/index.html` file in your browser to view the website.

## Usage

- Modify the `src/index.html` file to change the content of the website.
- Update `src/css/styles.css` to change the styles.
- Add functionality in `src/js/main.js`.

## Deployment

This project uses GitHub Actions to automatically deploy the website to GitHub Pages whenever changes are pushed to the repository. The workflow is defined in `.github/workflows/deploy.yml`.

## License

This project is licensed under the MIT License.