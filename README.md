- **An explanation of how data is scraped**  
  Used the GitHub API with Python’s requests library to retrieve data on users in Bangalore with over 100 followers, querying paginated results for detailed user and repository information while applying a delay to respect GitHub’s rate limits. Data fields, such as company names, were cleaned and formatted, and the finalized user and repository details were saved to CSV files.

- **The most interesting and surprising fact found after analyzing the data**  
  The most common language used across repositories is Jupyter Notebook, particularly for data science and machine learning projects, suggesting that data-centric development is popular.

- **Actionable recommendation for developers based on analysis** 
  A significant number of repositories lack licensing information, which can limit reuse and collaboration, as developers might be uncertain about usage rights. Adding clear licenses to repositories can encourage others to use, modify, and contribute to the projects, potentially increasing their impact and visibility.
