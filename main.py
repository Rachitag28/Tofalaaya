from fastapi import FastAPI
from routers import products, orders, items


app = FastAPI(
    title="TofaLaaya",
    version="0.0.1",
)

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(items.router)


@app.get("/healthcheck")
def root():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

