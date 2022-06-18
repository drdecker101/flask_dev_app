from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)



# To run script in Terminal
# C:/Users/<name>/Anaconda3/python.exe "c:/Users/<name>/Desktop/py/dev_world_06_2022/main.py"

# deploy app with heroku
# pip install gunicorn

# pip freeze > requirements.txt