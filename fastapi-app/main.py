from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def home():
    return {"msg": "Keep pushing :)"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
