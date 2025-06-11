# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from sys import stderr
from traceback import print_exc
from datetime import datetime
import asyncio

from flask import Flask, request, Response
from botbuilder.core import (
    ConversationState,
    BotFrameworkAdapterSettings,
    MemoryStorage,
    TurnContext,
    UserState,
    BotFrameworkAdapter,
)
from botbuilder.schema import Activity, ActivityTypes

from bots import UserPromptBot
from config import DefaultConfig

config = DefaultConfig()

app = Flask(__name__)
adapter_settings = BotFrameworkAdapterSettings(app_id=config.APP_ID, app_password=config.APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

storage = MemoryStorage()
conversation_state = ConversationState(storage)
user_state = UserState(storage)

bot = UserPromptBot(conversation_state, user_state)


async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=stderr)
    print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )
    # Send a trace activity if we're talking to the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        # Create a trace activity that contains the error object
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        # Send a trace activity, which will be displayed in Bot Framework Emulator
        await context.send_activity(trace_activity)

    # Clear out state
    await conversation_state.delete(context)

# Set the error handler on the Adapter.
adapter.on_turn_error = on_error


@app.route("/", methods=["GET"])
def home():
    return "Hello, World!"

@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = request.headers["Authorization"] if "Authorization" in request.headers else ""

    try:
        # Erstelle einen Event Loop für die asynchrone Ausführung
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Führe die asynchrone Funktion aus
        response = loop.run_until_complete(
            adapter.process_activity(activity, auth_header, bot.on_turn)
        )
        
        if response:
            return response
        return Response(status=201)
    except Exception as e:
        return Response(str(e), status=500)
    finally:
        loop.close()

if __name__ == "__main__":
    app.run(host=config.HOST, port=int(config.PORT))
