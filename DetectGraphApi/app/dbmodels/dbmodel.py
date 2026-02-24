from app.core.dbengine import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, text
import datetime
from typing import Annotated

intpk = Annotated[int, mapped_column(primary_key=True)]
s_time = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

class Detected_frames(Base):
    __tablename__ = "Detected_frames"
    __table_args__ = {"schema": "DetectionService"}

    id: Mapped[intpk]
    camera_id: Mapped[int]
    not_detected_minio_path: Mapped[str]
    detected_minio_path: Mapped[str]
    created_at: Mapped[s_time]

    detected_objects: list["Detected_objects"] = relationship(back_populates="frame")


class Detected_objects(Base):
    __tablename__ = "Detected_objects"
    __table_args__ = {"schema": "DetectionService"}

    id: Mapped[intpk]
    frame_id: Mapped[int] = mapped_column(ForeignKey("DetectionService.Detected_frames.id", ondelete='CASCADE'))
    camera_id: Mapped[int]
    label: Mapped[str]
    created_at: Mapped[s_time]
    score: Mapped[float]
    box_x1: Mapped[int]
    box_y1: Mapped[int]
    box_x2: Mapped[int]
    box_y2: Mapped[int]

    frame: Mapped["Detected_frames"] = relationship(back_populates="detected_objects", foreign_keys=[frame_id])







                


