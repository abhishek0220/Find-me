from dotenv import load_dotenv
import uvicorn
load_dotenv()


def runserver():
    from FindMe import app
    return app


app = runserver()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
