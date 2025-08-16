from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    """
    Create a new event

    Input (JSON):
      { "title": "Some Title" }

    Responses:
      201 Created  -> return the new event as JSON for successful POST
      400 Bad Req  -> return if the title missing/empty
    """
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    
     # Minimal validation based on simulated data/tests
    if not title:
        return jsonify({"error": "title is required"}), 400

    # Compute next id (max existing id + 1), default 0 if list empty
    next_id = (max((e.id for e in events), default=0) + 1)
    
    # Create, store, and return the new event
    new_event = Event(next_id, title)
    events.append(new_event)
    
    return jsonify(new_event.to_dict()), 201

# Update an existing event’s title
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    """
    Update fields on an existing event

    Input (JSON):
      { "title": "New Title" }

    Responses:
      200 OK        -> return updated event as JSON for PATCH
      404 Not Found -> return if event id does not exist
    """
    data = request.get_json(silent=True) or {}
    title = data.get("title")

    # Find the target event & update if found
    for e in events:
        if e.id == event_id:
            if title is not None:
                e.title = title
            return jsonify(e.to_dict()), 200

    # 404 error code if no event matched the id
    return jsonify({"error": "Event not found"}), 404

# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    """
    Delete an event by id

    Responses:
      204 No Content -> found and deleted the event successfully
      404 Not Found  -> return if event id does not exist
    """
    # iterate over the list while keeping both the index (i) and the item (e)
    for i, e in enumerate(events):
        if e.id == event_id:
            # remove the element at position i (which mutates the same 'events' list and doesn't return a new list)
            events.pop(i)
            return ("", 204)

    # 404 error code if no event matched the id
    return jsonify({"error": "Event not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
