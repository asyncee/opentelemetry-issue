from fastapi import FastAPI


def create_app(label):
    app = FastAPI(title=label)
    return app

