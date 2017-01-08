### Quick Start

1. Clone the repo
  ```
  $ git clone https://github.com/Elias-gg/CST-205-Proj3
  $ cd CST-205-Proj3
  ```

2. Initialize and activate a virtualenv:
  ```
  $ virtualenv -p python2.x --no-site-packages env
  $ source env/bin/activate

  * For windows
  virtualenv --python=C:\Python2X\python.exe --no-site-packages env

  env\Scripts\activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```
4. Create database
    ```
    $ python models.py

    *Download an SQLite browser if you are interested in exploring the database
    ```
5. Run the development server:
  ```
  $ python app.py
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000)
