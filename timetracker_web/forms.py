"""Form schemas for time tracker web app."""

from colander import MappingSchema, String, SchemaNode, Int

from .generic import Form


class CategorySchema(Form, MappingSchema):
    """Schema for editing categories."""

    title = SchemaNode(String())
    description = SchemaNode(String())


class TaskSchema(Form, MappingSchema):
    """Schema for editing tasks."""

    title = SchemaNode(String())
    description = SchemaNode(String())
    mins = SchemaNode(Int())
