from fastapi import FastAPI

from app.api.routes import router
## Set up sqlite db and save the logs there
# add async
# the log endpoint should have INFO and ERRORS, the others meh

app = FastAPI(
    title="Student Prompt Logger",
    version="0.1.0",
)

app.include_router(router)

def main():
    # See if you can make the user select the client from OpenAI
   
    # put each file in the correct folder/package
    print("API starting...")
    pass


if __name__ == "__main__":
    main()



