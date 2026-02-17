import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import uvicorn



@strawberry.type
class SingleCameraReport:
    camera_id: strawberry.ID
    last_description_time: str
    people_count_row: int
    is_weapon_detected: bool

@strawberry.type
class GeneralDailyReport:
    total_alerts_24h: int
    most_dangerous_camera_id: int
    status_overviev: str


@strawberry.type
class Query:
    @strawberry.field
    def get_camera_report(self, camera_id: int) -> SingleCameraReport:
        if camera_id == 1:
            return SingleCameraReport(
                camera_id=strawberry.ID("1"),
                last_description_time="2024-01-15 14:03:25",
                people_count_row=3,
                is_weapon_detected=True
            )
    
    @strawberry.field
    def get_general_report(self) -> GeneralDailyReport:
        return GeneralDailyReport(
            total_alerts_24h=10,
            most_dangerous_camera_id=1,
            status_overviev="Камера 1: 3 человека, оружия нет."
        )


schema = strawberry.Schema(query=Query)
app = FastAPI()
app.include_router(GraphQLRouter(schema=schema, graphql_ide=True), prefix="/graphql")

if __name__ == "__main__":
    uvicorn.run("test:app", reload=True)