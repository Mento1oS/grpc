# app/server.py
import logging
from concurrent import futures
import grpc
from google.protobuf import empty_pb2
from datetime import datetime

from proto import glossary_pb2, glossary_pb2_grpc

from .db import SessionLocal, engine, Base
from . import models, crud

# Создаём таблицы при старте (авто-миграция простого типа)
Base.metadata.create_all(bind=engine)

def to_proto_term(model_obj: models.Term) -> glossary_pb2.Term:
    return glossary_pb2.Term(
        id = model_obj.id,
        keyword = model_obj.keyword,
        definition = model_obj.definition,
        source = model_obj.source or "",
        created_at = model_obj.created_at.isoformat() if model_obj.created_at is not None else "",
        updated_at = model_obj.updated_at.isoformat() if model_obj.updated_at is not None else ""
    )

class GlossaryServicer(glossary_pb2_grpc.GlossaryServicer):
    def ListTerms(self, request, context):
        db = SessionLocal()
        try:
            rows = crud.get_terms(db)
            return glossary_pb2.TermList(terms=[to_proto_term(r) for r in rows])
        finally:
            db.close()

    def GetTermByKeyword(self, request, context):
        db = SessionLocal()
        try:
            r = crud.get_term_by_keyword(db, request.keyword)
            if not r:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Term not found")
                return glossary_pb2.Term()  # пустой
            return to_proto_term(r)
        finally:
            db.close()

    def GetTermById(self, request, context):
        db = SessionLocal()
        try:
            r = crud.get_term(db, request.id)
            if not r:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Term not found")
                return glossary_pb2.Term()
            return to_proto_term(r)
        finally:
            db.close()

    def CreateTerm(self, request, context):
        db = SessionLocal()
        try:
            existing = crud.get_term_by_keyword(db, request.keyword)
            if existing:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Term with this keyword already exists")
                return glossary_pb2.Term()
            created = crud.create_term(db, request.keyword, request.definition, request.source or None)
            return to_proto_term(created)
        finally:
            db.close()

    def UpdateTerm(self, request, context):
        db = SessionLocal()
        try:
            obj = crud.get_term(db, request.id)
            if not obj:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Term not found")
                return glossary_pb2.Term()
            updated = crud.update_term(db, obj,
                                       keyword=request.keyword or None,
                                       definition=request.definition or None,
                                       source=request.source or None)
            return to_proto_term(updated)
        finally:
            db.close()

    def DeleteTerm(self, request, context):
        db = SessionLocal()
        try:
            obj = crud.get_term(db, request.id)
            if not obj:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Term not found")
                return empty_pb2.Empty()
            crud.delete_term(db, obj)
            return empty_pb2.Empty()
        finally:
            db.close()

def serve(host='[::]', port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServicer_to_server(GlossaryServicer(), server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    logging.info(f"gRPC server started on {host}:{port}")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
