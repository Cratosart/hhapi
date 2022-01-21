# Programming vacancies compare  
  
  
The program searches for current vacancies on the portals and displays them in the console in the form of a table.  
  
  
### How to install  
  
Python3 must already be installed.  
Then use 'pip' to install the dependencies.  
  
```  
  
pip install -r requirements.txt  
  
```  
```  
py main.py  
```  
  
### Environment variables  
  
The program takes key from environment variable.  
Place the .env file in the root directory with the following options:  
  
  
```  
API_KEY_SJ=there must be a SuperJob API key  
  
```  
  
API_KEY_SJ=used to connect to API SuperJob for example:  
```  
v3.r.15029133.2ff49f9a025d973798236d8e53264e253854ab29.5e9687b65b85e460306e83c5b8c97a858f8b4eb3  
```  
  
It is recommended to use virtualenv/venv (https://docs.python.org/3/library/venv.html) to isolate the project.  
  
  
### Project Goals  
  
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).