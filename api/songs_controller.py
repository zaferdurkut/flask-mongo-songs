from random import randrange

import bson
from flask import jsonify, Blueprint, Response, abort, make_response
from flask_pydantic import validate

from api.dto.create_song_output_model import CreateSongOutputModel
from api.dto.list_songs_query_input_model import ListSongsQueryModel
from api.dto.song_input_model import SongInputModel
from api.dto.song_output_model import ListSongOutputModel
from api.dto.song_rating_input_model import SongRatingInputModel
from api.dto.song_score_output_model import SongScoreOutputModel
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


@blueprint_songs.route("/<song_id>/score", methods=["GET"])
def get_song_score_with_id(song_id: str) -> SongScoreOutputModel:
    if not bson.objectid.ObjectId.is_valid(song_id):
        response = make_response(jsonify(message="Invalid ID"), 400)
        abort(response)
    return jsonify(songs_manager.get_song_score_with_id(song_id=song_id).dict())


@blueprint_songs.route("/<song_id>/rating", methods=["PUT"])
@validate()
def add_rating(song_id: str, body: SongRatingInputModel):
    if not bson.objectid.ObjectId.is_valid(song_id):
        response = make_response(jsonify(message="Invalid ID"), 400)
        abort(response)
    songs_manager.add_rating(song_id=song_id, rating=body.rating)
    return Response(
        "",
        status=204,
        mimetype="application/json",
    )


@blueprint_songs.route("/initial", methods=["GET"])
def initial_songs():
    for song in INITIAL_SONGS:
        songs_manager.create_song(song=SongInputModel(**song))
    return Response(
        "",
        status=204,
        mimetype="application/json",
    )
