  # Monthly Dollar Change vs. Inflation Analysis

  This project contains two Python scripts that analyze the monthly change in the dollar and compare it with inflation using data from the National Institute of Statistics of Uruguay.

  ## Script Descriptions

  ### Analysis and Visualization Script

  This script downloads inflation and dollar exchange rate data, calculates monthly changes, and generates a bar chart comparing the dollar change with inflation.

  - **Data Sources**: 
    - IPC: [INE Uruguay](https://www5.ine.gub.uy)
    - Currency Exchange Rates: [INE Uruguay](https://www5.ine.gub.uy)

  - **Libraries Used**:
    - `requests`: For downloading files from the web.
    - `pandas`: For data manipulation.
    - `matplotlib`: For data visualization.

  - **Instructions**:
    1. Run the script to download the data and generate the chart.
    2. The chart is automatically saved as `cambio_dolar_vs_inflacion.png` in the current directory.

  ### Data Preparation Script

  This script prepares the data by downloading the necessary files and processing them for analysis.

  - **Libraries Used**:
    - `requests`: For downloading files from the web.
    - `pandas`: For data manipulation.

  - **Instructions**:
    1. Run the script to download and prepare the data for analysis.

  ## Requirements

  - Python 3.x
  - Libraries: `requests`, `pandas`, `matplotlib`

  ## Installation

  You can install the necessary libraries using `pip`:

  ```bash
  pip install requests pandas matplotlib
  ```

  ## License

  This project is licensed under the GNU Affero General Public License, version 3.0. For more details, see the `LICENSE` file.

  ## Contact

  For questions or comments, please contact [free4fun@riseup.net].
