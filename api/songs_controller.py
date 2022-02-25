from flask import jsonify, Blueprint, Response
from flask_pydantic import validate

from api.dto.create_song_output_model import CreateSongOutputModel
from api.dto.list_songs_query_input_model import ListSongsQueryModel
from api.dto.song_input_model import SongInputModel
from api.dto.song_output_model import ListSongOutputModel
from initial_songs import INITIAL_SONGS
from manager.songs_manager import SongsManager

blueprint_songs = Blueprint("/api/songs", __name__, url_prefix="/api/songs")


songs_manager: SongsManager = SongsManager()


@blueprint_songs.route("", methods=["GET"])
@validate()
def list_songs(query: ListSongsQueryModel) -> ListSongOutputModel:
    return jsonify(songs_manager.list_songs(query=query).dict())


@blueprint_songs.route("", methods=["POST"])
@validate()
def create_song(body: SongInputModel):
    return CreateSongOutputModel(id=songs_manager.create_song(song=body))


@blueprint_songs.route("/initial", methods=["GET"])
def initial_songs():
    for song in INITIAL_SONGS:
        songs_manager.create_song(song=SongInputModel(**song))
    return Response(
        "",
        status=204,
        mimetype="application/json",
    )
