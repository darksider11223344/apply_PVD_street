--- Create table Vehicle

Create Table tblVehicles
(
ID int NOT NULL IDENTITY(1,1),
VerhicleID nvarchar(50) NOT NULL,
TimeStampUTC DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
RouteId nvarchar(50) NOT NULL,
DepartLane nvarchar(50) NOT NULL,
TypeID nvarchar(50) NOT NULL,
Active bit NOT NULL
)

--- insert for demo
USE [PVD_traffic_data]
GO

INSERT INTO [dbo].[tblVehicles]
           ([VerhicleID]
           ,[RouteId]
           ,[DepartLane]
           ,[TypeID]
           ,[Active])
     VALUES
           ('vehicle_1'
           ,'route_0'
           ,'free'
           ,'vtype_car1'
           ,0)
GO