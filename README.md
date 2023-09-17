--- Create table Vehicle

Create Table tblVehicles
(
ID int NOT NULL IDENTITY(1,1),
VerhicleID nvarchar(50) NOT NULL,
TimeStampUTC DATETIME NULL,
RouteId nvarchar(50) NOT NULL,
DepartLane nvarchar(50) NOT NULL,
TypeID nvarchar(50) NOT NULL
)