import uvicorn
import os


def main():
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("ENV", "development") == "development"

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=reload,
        workers=1 if reload else 4
    )


if __name__ == "__main__":
    main()
