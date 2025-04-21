"""
This module provides utility functions for handling file uploads and messaging  in a video-to-mp3 conversion service.
"""

import os, pika, json

from gridfs import GridFS
import pika.spec
from werkzeug.datastructures import FileStorage
from pika.adapters.blocking_connection import BlockingChannel

def upload(f: FileStorage, fs: GridFS, channel: BlockingChannel, access: any) -> tuple[str, int]:
    try:
        fid = fs.put(f)
    except Exception as err:
        return f"internal server error: {str(err)}", 500
    
    message = { "video_fid": str(fid), "mp3_fid": None, "username": access["username"] }
    try:
        channel.basic_publish(
            exchange=os.environ.get("RABBITMQ_UPLOAD_EXCHANGE"), 
            routing_key=os.environ.get("RABBITMQ_UPLOAD_ROUTING_KEY"), 
            body=json.dumps(message), 
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as err:
        fs.delete(file_id=fid)
        return f"internal server error: {str(err)}", 500
    