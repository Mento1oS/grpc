# client.py
import grpc
from google.protobuf import empty_pb2
from proto import glossary_pb2, glossary_pb2_grpc

def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = glossary_pb2_grpc.GlossaryStub(channel)

    # Create a term
    req = glossary_pb2.CreateTermRequest(
        keyword="memoization",
        definition="Сохранение результатов вычислений для повторного использования.",
        source="notes"
    )
    try:
        term = stub.CreateTerm(req)
        print("Created:", term)
    except grpc.RpcError as e:
        print("CreateTerm error:", e.code(), e.details())

    # List terms
    terms = stub.ListTerms(empty_pb2.Empty())
    print("List:", terms)

    # Get by keyword
    try:
        got = stub.GetTermByKeyword(glossary_pb2.GetByKeywordRequest(keyword="memoization"))
        print("Get by keyword:", got)
    except grpc.RpcError as e:
        print("Get error:", e.code(), e.details())

    # Update
    try:
        updated = stub.UpdateTerm(glossary_pb2.UpdateTermRequest(
            id=term.id,
            definition="Обновлённое определение."
        ))
        print("Updated:", updated)
    except grpc.RpcError as e:
        print("Update error:", e.code(), e.details())

    # Delete
    try:
        stub.DeleteTerm(glossary_pb2.DeleteTermRequest(id=term.id))
        print("Deleted term id=", term.id)
    except grpc.RpcError as e:
        print("Delete error:", e.code(), e.details())

if __name__ == "__main__":
    run()
