import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import (
    date,
)  # TODO(autogpt): "date" is unknown import symbol. reportAttributeAccessIssue
from typing import Dict, List, Mapping, Optional

import prisma
import prisma.enums
import project.addInventoryItem_service
import project.addStaff_service
import project.addSupplier_service
import project.addSupplyChainItem_service
import project.authenticateUser_service
import project.createCustomer_service
import project.createCustomReport_service
import project.createFarmLayout_service
import project.createOrder_service
import project.createRole_service
import project.createSalesRecord_service
import project.createSchedule_service
import project.createUser_service
import project.deleteCustomer_service
import project.deleteFarmLayout_service
import project.deleteInventoryItem_service
import project.deleteOrder_service
import project.deleteRole_service
import project.deleteSalesRecord_service
import project.deleteSchedule_service
import project.deleteStaff_service
import project.deleteSupplyChainItem_service
import project.deleteUser_service
import project.getCustomer_service
import project.getFarmLayouts_service
import project.getFieldDetails_service
import project.getFinancialReports_service
import project.getInventory_service
import project.getInventoryItemDetails_service
import project.getInventoryReports_service
import project.getOperationalReports_service
import project.getOrder_service
import project.getSalesData_service
import project.getSalesTrends_service
import project.getScheduleById_service
import project.getSchedules_service
import project.getStaffDetails_service
import project.getSuppliers_service
import project.getSupplyChainItems_service
import project.getUser_service
import project.listCustomers_service
import project.listOrders_service
import project.listRoles_service
import project.listStaff_service
import project.listUsers_service
import project.refreshSession_service
import project.updateCustomer_service
import project.updateFarmLayout_service
import project.updateFieldDetails_service
import project.updateInventoryItem_service
import project.updateOrder_service
import project.updateRole_service
import project.updateSalesRecord_service
import project.updateSchedule_service
import project.updateStaff_service
import project.updateSupplier_service
import project.updateSupplyChainItem_service
import project.updateUser_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="tets",
    lifespan=lifespan,
    description="build this hristmastreefarm Inventory Management - Provides tools to manage tree stock, track inventory levels, and update statuses, including items like fertilizer, dirt, saplings, hoses, trucks, harvesters, lights, etc. Sales Tracking - Track sales data, analyze trends, and integrate with QuickBooks for financial management. Scheduling - Manage planting, harvesting, and delivery schedules. Customer Management - Maintain customer records, preferences, and order history integrated with Quickbooks. Order Management - Streamline order processing, from placement to delivery, integrated with QuickBooks for invoicing. Supply Chain Management - Oversees the supply chain from seedling purchase to delivery of trees. Reporting and Analytics - Generate detailed reports and analytics to support business decisions, directly linked with QuickBooks for accurate financial reporting. Mapping and Field Management - Map farm layouts, manage field assignments and track conditions of specific areas. Health Management - Monitor the health of the trees and schedule treatments. Staff Roles Management - Define roles, responsibilities, and permissions for all staff members. Staff Scheduling - Manage schedules for staff operations, ensuring coverage and efficiency. Staff Performance Management - Evaluate staff performance, set objectives, and provide feedback. Payroll Management - Automate payroll calculations, adhere to tax policies, and integrate with QuickBooks. QuickBooks Integration - Integrate seamlessly across all financial aspects of the app to ensure comprehensive financial management.",
)


@app.delete(
    "/users/{userId}", response_model=project.deleteUser_service.DeleteUserResponse
)
async def api_delete_deleteUser(
    userId: int,
) -> project.deleteUser_service.DeleteUserResponse | Response:
    """
    Deletes a user account based on the user ID provided in the path. Used for removing former employees or incorrect entries. Operation logs entries for accountability.
    """
    try:
        res = project.deleteUser_service.deleteUser(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/sales/{salesId}",
    response_model=project.updateSalesRecord_service.UpdateSalesResponse,
)
async def api_put_updateSalesRecord(
    salesId: int, total: float, status: prisma.enums.OrderStatus, date: datetime
) -> project.updateSalesRecord_service.UpdateSalesResponse | Response:
    """
    Updates an existing sales record. Parameters include sales ID and the new sales data fields to be updated. The system recalculates related financial entries and updates QuickBooks accordingly. Expected response is success confirmation along with updated record details.
    """
    try:
        res = project.updateSalesRecord_service.updateSalesRecord(
            salesId, total, status, date
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/supply-chain/suppliers",
    response_model=project.addSupplier_service.SupplierRegistrationResponse,
)
async def api_post_addSupplier(
    name: str, contact: str, types_of_goods: List[str]
) -> project.addSupplier_service.SupplierRegistrationResponse | Response:
    """
    Registers a new supplier in the system. Essential for expanding the range of goods available for farm operations. Details required include supplier name, contact information, and types of goods supplied. This endpoint helps to diversify the farm’s supply chain and mitigate risks by not relying on a single supplier.
    """
    try:
        res = project.addSupplier_service.addSupplier(name, contact, types_of_goods)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/api/staff", response_model=project.addStaff_service.AddStaffResponse)
async def api_post_addStaff(
    firstName: str,
    lastName: str,
    email: str,
    phone: Optional[str],
    role: prisma.enums.Role,
    hashedPassword: str,
) -> project.addStaff_service.AddStaffResponse | Response:
    """
    Adds a new staff member to the system. Requires input of personal details, role, and permissions. Ensures data consistency through validations and role checking with User Management.
    """
    try:
        res = await project.addStaff_service.addStaff(
            firstName, lastName, email, phone, role, hashedPassword
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/api/roles", response_model=project.listRoles_service.GetRolesResponse)
async def api_get_listRoles(
    request: project.listRoles_service.GetRolesRequest,
) -> project.listRoles_service.GetRolesResponse | Response:
    """
    Provides a list of all staff roles and associated permissions, aiding in access control and role assignments. Accessible by Admin and HR for management and oversight.
    """
    try:
        res = await project.listRoles_service.listRoles(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/inventory", response_model=project.getInventory_service.InventoryListResponse
)
async def api_get_getInventory(
    type: Optional[str], status: Optional[str]
) -> project.getInventory_service.InventoryListResponse | Response:
    """
    Retrieves the current stock levels of all inventory items including trees, fertilizers, and other related items. This function uses queries to filter data based on item type, status, and other parameters. Expected to respond with a list of items, their quantities, and statuses.
    """
    try:
        res = await project.getInventory_service.getInventory(type, status)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/api/farm-layouts/{layoutId}",
    response_model=project.updateFarmLayout_service.UpdateFarmLayoutResponse,
)
async def api_put_updateFarmLayout(
    layoutId: int,
    name: Optional[str],
    areaSize: Optional[float],
    mapUrl: Optional[str],
    condition: Optional[prisma.enums.FieldCondition],
) -> project.updateFarmLayout_service.UpdateFarmLayoutResponse | Response:
    """
    Updates an existing farm layout. It requires layoutId as path parameter and updates fields based on the submitted data. Changes might include reassignment of areas or updates in layout dimensions, maintained through GIS standards.
    """
    try:
        res = await project.updateFarmLayout_service.updateFarmLayout(
            layoutId, name, areaSize, mapUrl, condition
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/inventory",
    response_model=project.addInventoryItem_service.InventoryAdditionResponse,
)
async def api_post_addInventoryItem(
    name: str, quantity: int, type: prisma.enums.InventoryType
) -> project.addInventoryItem_service.InventoryAdditionResponse | Response:
    """
    Adds a new item to the inventory following receipt of stocks, such as new tree saplings or farming tools. It requires details like item name, quantity, and category. Success response includes confirmation of addition and the new inventory state.
    """
    try:
        res = project.addInventoryItem_service.addInventoryItem(name, quantity, type)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/supply-chain/items",
    response_model=project.addSupplyChainItem_service.AddSupplyChainItemResponse,
)
async def api_post_addSupplyChainItem(
    item_name: str,
    quantity: int,
    supplier: str,
    expected_delivery_date: datetime,
    type: prisma.enums.InventoryType,
    status: prisma.enums.InventoryStatus,
) -> project.addSupplyChainItem_service.AddSupplyChainItemResponse | Response:
    """
    Adds a new item to the supply chain database. This is necessary for updating the inventory with new types of seedlings or farming supplies. The endpoint requires details such as item name, quantity, supplier, and expected delivery date. It directly interacts with the Inventory Management module to update stock levels once the items are delivered.
    """
    try:
        res = project.addSupplyChainItem_service.addSupplyChainItem(
            item_name, quantity, supplier, expected_delivery_date, type, status
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/orders", response_model=project.createOrder_service.CreateOrderResponse)
async def api_post_createOrder(
    customerId: int,
    items: List[project.createOrder_service.OrderItem],
    deliveryDate: datetime,
) -> project.createOrder_service.CreateOrderResponse | Response:
    """
    Creates a new order. This endpoint extracts customer preferences from the Customer Management module, checks product availability from the Inventory Management module, and initializes an order. It interacts with QuickBooks through API to set up invoicing. The response includes the order ID and confirmation of creation.
    """
    try:
        res = project.createOrder_service.createOrder(customerId, items, deliveryDate)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/schedules/{scheduleId}",
    response_model=project.updateSchedule_service.ScheduleResponse,
)
async def api_put_updateSchedule(
    scheduleId: int,
    date: datetime,
    activityType: prisma.enums.ActivityType,
    fieldId: Optional[int],
    resources: List[int],
) -> project.updateSchedule_service.ScheduleResponse | Response:
    """
    Updates an existing schedule identified by scheduleId. This can include changes to time, date, resources involved, or activity type. Ensures consistency and feasibility by checking current field statuses and resource availability analogous to the schedule creation process.
    """
    try:
        res = project.updateSchedule_service.updateSchedule(
            scheduleId, date, activityType, fieldId, resources
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/api/farm-layouts/{layoutId}",
    response_model=project.deleteFarmLayout_service.DeleteFarmLayoutResponse,
)
async def api_delete_deleteFarmLayout(
    layoutId: str, confirmDeletion: bool
) -> project.deleteFarmLayout_service.DeleteFarmLayoutResponse | Response:
    """
    Deletes a specific farm layout identified by layoutId. It removes all related data from the system and should confirm the deletion to avoid accidental loss of data.
    """
    try:
        res = project.deleteFarmLayout_service.deleteFarmLayout(
            layoutId, confirmDeletion
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/refresh", response_model=project.refreshSession_service.AuthRefreshResponse
)
async def api_post_refreshSession(
    Authorization: str,
) -> project.refreshSession_service.AuthRefreshResponse | Response:
    """
    Refreshes the authentication session by issuing a new token. Requires a valid JWT in the request header. Helps maintain user session continuity safely.
    """
    try:
        res = project.refreshSession_service.refreshSession(Authorization)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/api/supply-chain/suppliers/{supplierId}",
    response_model=project.updateSupplier_service.UpdateSupplierResponse,
)
async def api_put_updateSupplier(
    supplierId: int,
    name: str,
    contactName: str,
    contactEmail: str,
    contactPhone: str,
    address: str,
) -> project.updateSupplier_service.UpdateSupplierResponse | Response:
    """
    Updates existing supplier information. This is crucial for keeping supplier details current, which is essential for ongoing supply chain management. Ensures communication and orders are directed correctly and helps maintain strong supplier relationships.
    """
    try:
        res = await project.updateSupplier_service.updateSupplier(
            supplierId, name, contactName, contactEmail, contactPhone, address
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/farm-layouts",
    response_model=project.getFarmLayouts_service.GetFarmLayoutResponse,
)
async def api_get_getFarmLayouts(
    request: project.getFarmLayouts_service.GetFarmLayoutRequest,
) -> project.getFarmLayouts_service.GetFarmLayoutResponse | Response:
    """
    Retrieves all farm layouts. Expected to return a detailed map of the farm layout including field identifiers and conditions. It will leverage GIS mapping functionalities to present a spatial view of the premises.
    """
    try:
        res = await project.getFarmLayouts_service.getFarmLayouts(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/api/roles", response_model=project.createRole_service.CreateRoleResponse)
async def api_post_createRole(
    role_name: str, permissions: str
) -> project.createRole_service.CreateRoleResponse | Response:
    """
    Creates a new staff role with specific permissions. Facilitates dynamic role creation based on organizational needs, controlled by Admin and HR.
    """
    try:
        res = project.createRole_service.createRole(role_name, permissions)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/reports/inventory",
    response_model=project.getInventoryReports_service.InventoryReportResponse,
)
async def api_get_getInventoryReports(
    type: Optional[prisma.enums.InventoryType],
    status: Optional[prisma.enums.InventoryStatus],
) -> project.getInventoryReports_service.InventoryReportResponse | Response:
    """
    Generates detailed inventory reports which provide insights into stock levels, usage trends, and reordering necessities. This report utilizes data from the Inventory Management module to offer real-time tracking and projections. Expected response is a structured JSON with inventory items categorized and quantified, helping in making informed stocking decisions.
    """
    try:
        res = project.getInventoryReports_service.getInventoryReports(type, status)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/orders/{orderId}", response_model=project.updateOrder_service.UpdateOrderResponse
)
async def api_put_updateOrder(
    orderId: int,
    new_status: prisma.enums.OrderStatus,
    items: List[project.updateOrder_service.OrderItemUpdate],
    customer_comments: Optional[str],
) -> project.updateOrder_service.UpdateOrderResponse | Response:
    """
    Updates the details of an existing order. This is useful for changes in order quantities, customer requests, or cancellations. Updates will affect stock levels in the Inventory Management module and are reflected in financial records in QuickBooks.
    """
    try:
        res = project.updateOrder_service.updateOrder(
            orderId, new_status, items, customer_comments
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/orders/{orderId}", response_model=project.deleteOrder_service.DeleteOrderResponse
)
async def api_delete_deleteOrder(
    orderId: int, confirmation: bool
) -> project.deleteOrder_service.DeleteOrderResponse | Response:
    """
    Deletes an existing order. This will release the reserved inventory back to the Inventory Management system and update the financial records in QuickBooks to reflect the cancellation. This action requires confirmation from an authorized user.
    """
    try:
        res = await project.deleteOrder_service.deleteOrder(orderId, confirmation)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/api/staff/{id}", response_model=project.deleteStaff_service.DeleteStaffResponse
)
async def api_delete_deleteStaff(
    id: int,
) -> project.deleteStaff_service.DeleteStaffResponse | Response:
    """
    Deletes a staff member's record from the system. Restricted solely to Admin and HR to ensure security and control over staffing changes.
    """
    try:
        res = await project.deleteStaff_service.deleteStaff(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users", response_model=project.createUser_service.CreateUserResponse)
async def api_post_createUser(
    username: str, email: str, password: str
) -> project.createUser_service.CreateUserResponse | Response:
    """
    Creates a new user account. Expects user details such as username, email, and password in the request body. Returns the created user's ID and basic information. It assigns a default role until further updated. Utilizes hashing for password storage.
    """
    try:
        res = await project.createUser_service.createUser(username, email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/customers", response_model=project.listCustomers_service.GetCustomersResponse
)
async def api_get_listCustomers(
    name: Optional[str],
    email: Optional[str],
    page: Optional[int],
    pageSize: Optional[int],
) -> project.listCustomers_service.GetCustomersResponse | Response:
    """
    Lists all customers in the system. This endpoint is useful for administrative and management purposes to overview all client interactions and histories. Returns a JSON list of customer objects.
    """
    try:
        res = project.listCustomers_service.listCustomers(name, email, page, pageSize)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/api/roles/{id}", response_model=project.deleteRole_service.DeleteRoleResponse
)
async def api_delete_deleteRole(
    id: int,
) -> project.deleteRole_service.DeleteRoleResponse | Response:
    """
    Removes a set role from the system, maintaining clean and up-to-date role management. Access limited to Admin and HR for security reasons.
    """
    try:
        res = await project.deleteRole_service.deleteRole(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/schedules", response_model=project.getSchedules_service.GetSchedulesResponse)
async def api_get_getSchedules(
    request: project.getSchedules_service.GetSchedulesRequest,
) -> project.getSchedules_service.GetSchedulesResponse | Response:
    """
    Retrieves a list of all scheduling events, including planting, harvesting, and delivery schedules. Each schedule entry contains relevant details such as date, time, activity type, and related field location or resources involved. This endpoint also utilizes information from the Mapping and Field Management module to provide context on field conditions.
    """
    try:
        res = await project.getSchedules_service.getSchedules(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/orders", response_model=project.listOrders_service.OrdersListResponse)
async def api_get_listOrders(
    status: Optional[prisma.enums.OrderStatus],
    start_date: Optional[date],
    end_date: Optional[date],
    customer_id: Optional[int],
    product_ids: Optional[List[int]],
) -> project.listOrders_service.OrdersListResponse | Response:
    """
    Lists all orders with options to filter by status, date, customer, or products. Useful for managerial oversight and operational planning. Each listed order includes key details for quick assessment and further actions.
    """
    try:
        res = project.listOrders_service.listOrders(
            status, start_date, end_date, customer_id, product_ids
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/inventory/{itemId}",
    response_model=project.updateInventoryItem_service.UpdateInventoryItemResponse,
)
async def api_put_updateInventoryItem(
    itemId: int, quantity: Optional[int], status: prisma.enums.InventoryStatus
) -> project.updateInventoryItem_service.UpdateInventoryItemResponse | Response:
    """
    Updates existing inventory items, such as editing quantity after a sale or order processing. This endpoint requires the item ID and new data such as quantity or status. The response confirms the update and shows the edited item details.
    """
    try:
        res = project.updateInventoryItem_service.updateInventoryItem(
            itemId, quantity, status
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.patch(
    "/api/fields/{fieldId}",
    response_model=project.updateFieldDetails_service.UpdateFieldResponse,
)
async def api_patch_updateFieldDetails(
    fieldId: int,
    name: Optional[str],
    areaSize: Optional[float],
    mapUrl: Optional[str],
    condition: Optional[prisma.enums.FieldCondition],
) -> project.updateFieldDetails_service.UpdateFieldResponse | Response:
    """
    Updates specific attributes of a field, targeted with fieldId. This could include changes in crop types, planting dates or updating area conditions. This endpoint ensures the field data is up-to-date for operational efficiency.
    """
    try:
        res = project.updateFieldDetails_service.updateFieldDetails(
            fieldId, name, areaSize, mapUrl, condition
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/farm-layouts",
    response_model=project.createFarmLayout_service.CreateFarmLayoutResponse,
)
async def api_post_createFarmLayout(
    layout_name: str,
    dimensions: project.createFarmLayout_service.Dimension,
    paths: List[project.createFarmLayout_service.Path],
    fields: List[project.createFarmLayout_service.FieldArea],
) -> project.createFarmLayout_service.CreateFarmLayoutResponse | Response:
    """
    Creates a new farm layout. Accepts layout data including dimensions, paths, and designated field areas. This function uses GIS data formats for high accuracy and interacts with a database to store layout details.
    """
    try:
        res = project.createFarmLayout_service.createFarmLayout(
            layout_name, dimensions, paths, fields
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/reports/operational",
    response_model=project.getOperationalReports_service.OperationalReportsResponse,
)
async def api_get_getOperationalReports(
    start_date: datetime, end_date: datetime, role: Optional[str]
) -> project.getOperationalReports_service.OperationalReportsResponse | Response:
    """
    Focuses on providing comprehensive operational reports. Details include productivity, scheduling efficiency, and resource allocation based on data from Scheduling and Staff Roles Management modules. This route is designed to deliver a JSON response with statistical and graphical representations of operational performance.
    """
    try:
        res = await project.getOperationalReports_service.getOperationalReports(
            start_date, end_date, role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/sales", response_model=project.createSalesRecord_service.SalesRecordResponse
)
async def api_post_createSalesRecord(
    items_sold: List[int],
    customer_id: int,
    total_amount: float,
    transaction_details: project.createSalesRecord_service.TransactionDetails,
) -> project.createSalesRecord_service.SalesRecordResponse | Response:
    """
    Adds a new sales record to the system. This endpoint accepts sales data, including details of the items sold, customer information, and transaction amount. It updates the system and QuickBooks post validation of the data received from Order Management. Expected response confirms successful creation with a reference to the new sales record ID.
    """
    try:
        res = await project.createSalesRecord_service.createSalesRecord(
            items_sold, customer_id, total_amount, transaction_details
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/api/staff", response_model=project.listStaff_service.StaffListResponse)
async def api_get_listStaff(
    request: project.listStaff_service.GetStaffListRequest,
) -> project.listStaff_service.StaffListResponse | Response:
    """
    Retrieves a list of all staff members along with their basic details. Integrates with User Management to ensure only authorized viewing based on user roles like Admin and HR.
    """
    try:
        res = await project.listStaff_service.listStaff(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/sales/{salesId}",
    response_model=project.deleteSalesRecord_service.DeleteSalesResponse,
)
async def api_delete_deleteSalesRecord(
    salesId: int,
) -> project.deleteSalesRecord_service.DeleteSalesResponse | Response:
    """
    Deletes a specific sales record identified by the sales ID. This removal also adjusts the inventory and financial data within QuickBooks to reflect the change. Expected response is a success message confirming the deletion of the record.
    """
    try:
        res = await project.deleteSalesRecord_service.deleteSalesRecord(salesId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/inventory/{itemId}",
    response_model=project.deleteInventoryItem_service.DeleteInventoryItemResponse,
)
async def api_delete_deleteInventoryItem(
    itemId: int,
) -> project.deleteInventoryItem_service.DeleteInventoryItemResponse | Response:
    """
    Deletes an item from inventory when it is no longer available or needed. This endpoint needs the item ID. A successful deletion will be confirmed along with an updated list of remaining inventory items.
    """
    try:
        res = await project.deleteInventoryItem_service.deleteInventoryItem(itemId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/customers/{id}",
    response_model=project.deleteCustomer_service.DeleteCustomerResponse,
)
async def api_delete_deleteCustomer(
    id: int, user_role: prisma.enums.Role
) -> project.deleteCustomer_service.DeleteCustomerResponse | Response:
    """
    Removes a customer's record from the database using their ID. This action will also trigger an update to remove the customer's information from QuickBooks and other integrated services, like Order Management, to maintain data integrity. Returns a success status upon successful deletion.
    """
    try:
        res = await project.deleteCustomer_service.deleteCustomer(id, user_role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/customers", response_model=project.createCustomer_service.CreateCustomerResponse
)
async def api_post_createCustomer(
    name: str,
    email: str,
    phone: Optional[str],
    address: str,
    preferences: str,
    quickBooksIntegrationDetails: Dict[str, str],
) -> project.createCustomer_service.CreateCustomerResponse | Response:
    """
    Creates a new customer record in the database. This endpoint accepts customer details such as name, contact information, and preferences, and persists them to the database. Also integrates with QuickBooks to initialize financial management settings for the new customer. Returns the created customer object with an ID.
    """
    try:
        res = await project.createCustomer_service.createCustomer(
            name, email, phone, address, preferences, quickBooksIntegrationDetails
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/customers/{id}",
    response_model=project.updateCustomer_service.UpdateCustomerResponse,
)
async def api_put_updateCustomer(
    name: str, id: str, email: str, phone: Optional[str], address: str, preferences: str
) -> project.updateCustomer_service.UpdateCustomerResponse | Response:
    """
    Updates an existing customer's record. Fields that can be updated include customer name, contact details, and preferences. This endpoint will also update the relevant details in QuickBooks and ensure that all data remains synchronized. Returns a success status and the updated customer data.
    """
    try:
        res = await project.updateCustomer_service.updateCustomer(
            name, id, email, phone, address, preferences
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users", response_model=project.listUsers_service.GetUsersResponse)
async def api_get_listUsers(
    page: int, pageSize: int, role: Optional[str], email: Optional[str]
) -> project.listUsers_service.GetUsersResponse | Response:
    """
    Lists all user profiles with pagination support. Optionally filters by role or other attributes if specified in the query. Primarily used by Admin and HR for oversight and management.
    """
    try:
        res = await project.listUsers_service.listUsers(page, pageSize, role, email)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/schedules/{scheduleId}",
    response_model=project.deleteSchedule_service.DeleteScheduleResponse,
)
async def api_delete_deleteSchedule(
    scheduleId: int,
) -> project.deleteSchedule_service.DeleteScheduleResponse | Response:
    """
    Deletes a schedule identified by the scheduleId. This action removes the schedule from the system and updates related resource allocations and field statuses accordingly.
    """
    try:
        res = await project.deleteSchedule_service.deleteSchedule(scheduleId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/reports/custom",
    response_model=project.createCustomReport_service.CustomReportResponse,
)
async def api_post_createCustomReport(
    report_type: str,
    date_range: Mapping[str, date],
    data_sources: List[str],
    group_by: List[str],
    order_by: List[str],
    aggregate_functions: Mapping[str, str],
    format: str,
) -> project.createCustomReport_service.CustomReportResponse | Response:
    """
    Allows users to generate custom reports based on specified parameters and data sources like Sales Tracking, Inventory, and Payroll. Users can define what data to aggregate and the format of reporting. Expect a JSON representation of the created report. This endpoint facilitates specialized reporting for unique business insights.
    """
    try:
        res = await project.createCustomReport_service.createCustomReport(
            report_type,
            date_range,
            data_sources,
            group_by,
            order_by,
            aggregate_functions,
            format,
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/api/supply-chain/items/{itemId}",
    response_model=project.deleteSupplyChainItem_service.DeleteInventoryItemResponse,
)
async def api_delete_deleteSupplyChainItem(
    itemId: int,
) -> project.deleteSupplyChainItem_service.DeleteInventoryItemResponse | Response:
    """
    Removes an item from the supply chain. This endpoint is used when an item is no longer needed or if the order was cancelled. It ensures the Supply Chain Management system remains clean and up-to-date, also reflecting changes in the Inventory Management system to keep stock levels accurate.
    """
    try:
        res = await project.deleteSupplyChainItem_service.deleteSupplyChainItem(itemId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/reports/financial",
    response_model=project.getFinancialReports_service.FinancialReportResponse,
)
async def api_get_getFinancialReports(
    startDate: Optional[date], endDate: Optional[date]
) -> project.getFinancialReports_service.FinancialReportResponse | Response:
    """
    Retrieves comprehensive financial reports using data from QuickBooks, Sales Tracking, and Inventory Management modules. This route compiles and presents financial data which includes sales, expenses, and profitability analytics. The expected response would be detailed JSON containing various financial indicators and their breakdowns. This integration ensures data accuracy and coherence across related modules.
    """
    try:
        res = await project.getFinancialReports_service.getFinancialReports(
            startDate, endDate
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/supply-chain/suppliers",
    response_model=project.getSuppliers_service.GetSuppliersResponse,
)
async def api_get_getSuppliers(
    request: project.getSuppliers_service.GetSuppliersRequest,
) -> project.getSuppliers_service.GetSuppliersResponse | Response:
    """
    Lists all suppliers associated with the farm's supply chain. Provides contact information, type of goods supplied, and historical ordering data. This endpoint is vital for managing relationships with suppliers and planning future purchases. It assists in making informed decisions based on past performance and reliability.
    """
    try:
        res = await project.getSuppliers_service.getSuppliers(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/supply-chain/items",
    response_model=project.getSupplyChainItems_service.GetSupplyChainItemsResponse,
)
async def api_get_getSupplyChainItems(
    request: project.getSupplyChainItems_service.GetSupplyChainItemsRequest,
) -> project.getSupplyChainItems_service.GetSupplyChainItemsResponse | Response:
    """
    Retrieves all items in the supply chain, including current stock levels, source details, and tracking information. This endpoint helps to monitor the overall supply chain flow and is essential for replenishment planning. It utilizes data from the Inventory Management module to accurately reflect stock levels and integrates with the Scheduling module to anticipate upcoming supply needs.
    """
    try:
        res = await project.getSupplyChainItems_service.getSupplyChainItems(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users/{userId}", response_model=project.getUser_service.UserProfileResponse)
async def api_get_getUser(
    userId: str,
) -> project.getUser_service.UserProfileResponse | Response:
    """
    Retrieves a user's profile based on the provided user ID in the path. Returns the user’s detailed information, excluding sensitive data like passwords. Useful for profile viewing and management operations.
    """
    try:
        res = await project.getUser_service.getUser(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/sales", response_model=project.getSalesData_service.SalesRecordListResponse)
async def api_get_getSalesData(
    request: project.getSalesData_service.FetchSalesDataRequest,
) -> project.getSalesData_service.SalesRecordListResponse | Response:
    """
    Retrieves a list of all sales records. This endpoint fetches detailed sales information, analyzes trends, and prepares data for financial reporting. The data is fetched in coordination with updates received from the Order Management module and is formatted for QuickBooks integration. Expected response includes arrays of sales records with details like transaction ID, date, amount, and related customer and product info.
    """
    try:
        res = await project.getSalesData_service.getSalesData(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/inventory/{itemId}",
    response_model=project.getInventoryItemDetails_service.InventoryItemResponse,
)
async def api_get_getInventoryItemDetails(
    itemId: int,
) -> project.getInventoryItemDetails_service.InventoryItemResponse | Response:
    """
    Fetches detailed information about a specific inventory item by item ID. Provides comprehensive details including quantity, status, last updated, and category. Useful for audits and detailed checks.
    """
    try:
        res = await project.getInventoryItemDetails_service.getInventoryItemDetails(
            itemId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/schedules", response_model=project.createSchedule_service.ScheduleCreationResponse
)
async def api_post_createSchedule(
    date: datetime,
    activityType: prisma.enums.ActivityType,
    staffDetailsId: Optional[int],
    fieldId: Optional[int],
    inventoryItemId: Optional[int],
) -> project.createSchedule_service.ScheduleCreationResponse | Response:
    """
    Creates a new scheduling event. Requires details such as date, time, type of activity (planting, harvesting, delivery), and associated resources or locations. The system checks for field availability and resource constraints by interacting with the Mapping and Field Management and Supply Chain Management modules before confirming the creation of the schedule.
    """
    try:
        res = await project.createSchedule_service.createSchedule(
            date, activityType, staffDetailsId, fieldId, inventoryItemId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/login", response_model=project.authenticateUser_service.LoginResponse)
async def api_post_authenticateUser(
    username: str, password: str
) -> project.authenticateUser_service.LoginResponse | Response:
    """
    Handles user authentication. Expects username and password in the request body. Returns a JSON Web Token (JWT) for session handling on successful authentication, along with user role and ID for role-based access throughout the app.
    """
    try:
        res = await project.authenticateUser_service.authenticateUser(
            username, password
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/api/supply-chain/items/{itemId}",
    response_model=project.updateSupplyChainItem_service.UpdateSupplyChainItemResponse,
)
async def api_put_updateSupplyChainItem(
    itemId: int, quantity: int, supplierName: str, expectedDelivery: datetime
) -> project.updateSupplyChainItem_service.UpdateSupplyChainItemResponse | Response:
    """
    Updates the details of an existing supply chain item. This can include changes to quantity, supplier information, and expected delivery dates. It is crucial for maintaining accurate and up-to-date information on the supplies necessary for farm operations. Changes here are reflected in the Inventory Management system for seamless stock updates.
    """
    try:
        res = await project.updateSupplyChainItem_service.updateSupplyChainItem(
            itemId, quantity, supplierName, expectedDelivery
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put("/users/{userId}", response_model=project.updateUser_service.UpdatedUserInfo)
async def api_put_updateUser(
    userId: int, email: str, firstName: str, lastName: str, role: prisma.enums.Role
) -> project.updateUser_service.UpdatedUserInfo | Response:
    """
    Updates user information such as email, name, or role. Requires user ID in the path and updated data fields in the request body. Returns updated information of the user. Ensures that sensitive changes like role updates are logged for security compliance.
    """
    try:
        res = await project.updateUser_service.updateUser(
            userId, email, firstName, lastName, role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/sales/trends",
    response_model=project.getSalesTrends_service.GetSalesTrendsResponse,
)
async def api_get_getSalesTrends(
    start_date: date, end_date: date, group_by: str
) -> project.getSalesTrends_service.GetSalesTrendsResponse | Response:
    """
    Analyzes and retrieves sales trends over a specified period. This route fetches data grouped by different metrics (e.g., monthly, by product) to aid in financial decision-making and report generation in QuickBooks. Expected response includes graphical data or structured trend analysis.
    """
    try:
        res = await project.getSalesTrends_service.getSalesTrends(
            start_date, end_date, group_by
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/staff/{id}",
    response_model=project.getStaffDetails_service.StaffDetailsResponse,
)
async def api_get_getStaffDetails(
    id: int,
) -> project.getStaffDetails_service.StaffDetailsResponse | Response:
    """
    Fetches detailed information of a single staff member using their ID. Only accessible to Admin, HR, and to the individual staff member when retrieving their own details.
    """
    try:
        res = await project.getStaffDetails_service.getStaffDetails(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/customers/{id}",
    response_model=project.getCustomer_service.GetCustomerDetailsResponse,
)
async def api_get_getCustomer(
    id: str,
) -> project.getCustomer_service.GetCustomerDetailsResponse | Response:
    """
    Retrieves detailed information about a specific customer using their unique ID. This information includes name, contact details, preferences, and historical transaction data. It will interact with QuickBooks to fetch financial data related to the customer and with Order Management to retrieve order history. Expected to return a JSON object containing the customer's information.
    """
    try:
        res = await project.getCustomer_service.getCustomer(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/schedules/{scheduleId}",
    response_model=project.getScheduleById_service.ScheduleDetailsResponse,
)
async def api_get_getScheduleById(
    scheduleId: int,
) -> project.getScheduleById_service.ScheduleDetailsResponse | Response:
    """
    Retrieves detailed information about a specific schedule by scheduleId. This includes all details like associated date, time, activity, involved resources or fields, and any pertinent notes or updates from staff.
    """
    try:
        res = await project.getScheduleById_service.getScheduleById(scheduleId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.patch(
    "/api/roles/{id}", response_model=project.updateRole_service.RoleUpdateResponse
)
async def api_patch_updateRole(
    id: str, new_permissions: List[str]
) -> project.updateRole_service.RoleUpdateResponse | Response:
    """
    Updates the permissions associated with a specific role. Ensures role adaptability to evolving organizational policies, with changes authenticated and limited to Admin and HR.
    """
    try:
        res = await project.updateRole_service.updateRole(id, new_permissions)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/orders/{orderId}", response_model=project.getOrder_service.OrderDetailsResponse
)
async def api_get_getOrder(
    orderId: int,
) -> project.getOrder_service.OrderDetailsResponse | Response:
    """
    Retrieves detailed information of a specific order by ID. It provides comprehensive data including items, quantities, customer details, and invoicing status from QuickBooks. Ensures synchronization with Inventory statuses and updates Customer Management records as needed.
    """
    try:
        res = await project.getOrder_service.getOrder(orderId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/fields/{fieldId}",
    response_model=project.getFieldDetails_service.FieldDetailsResponse,
)
async def api_get_getFieldDetails(
    fieldId: int,
) -> project.getFieldDetails_service.FieldDetailsResponse | Response:
    """
    Fetches details of a specific field including soil type, crop status, and recent activities by passing fieldId. Useful for monitoring and deploying field workers as per requirements.
    """
    try:
        res = await project.getFieldDetails_service.getFieldDetails(fieldId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/api/staff/{id}", response_model=project.updateStaff_service.StaffUpdateResponse
)
async def api_put_updateStaff(
    id: int,
    email: str,
    firstName: str,
    lastName: str,
    phone: Optional[str],
    role: prisma.enums.Role,
) -> project.updateStaff_service.StaffUpdateResponse | Response:
    """
    Updates the details of an existing staff member. Only Admin and HR can edit roles and permissions, while self-update is limited to personal information by the staff themselves.
    """
    try:
        res = await project.updateStaff_service.updateStaff(
            id, email, firstName, lastName, phone, role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
