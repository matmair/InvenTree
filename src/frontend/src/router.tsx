import {
  Outlet,
  createRootRoute,
  createRoute,
  createRouter,
  redirect
} from '@tanstack/react-router';
import { lazy } from 'react';

import { Loadable } from './functions/loading';

// Lazy loaded pages
const LayoutComponent = Loadable(
  lazy(() => import('./components/nav/Layout')),
  true,
  true
);
const LoginLayoutComponent = Loadable(
  lazy(() => import('./pages/Auth/Layout')),
  true,
  true
);

const Home = Loadable(lazy(() => import('./pages/Index/Home')));

const CompanyDetail = Loadable(
  lazy(() => import('./pages/company/CompanyDetail'))
);

const CustomerDetail = Loadable(
  lazy(() => import('./pages/company/CustomerDetail'))
);

const SupplierDetail = Loadable(
  lazy(() => import('./pages/company/SupplierDetail'))
);

const ManufacturerDetail = Loadable(
  lazy(() => import('./pages/company/ManufacturerDetail'))
);

const SupplierPartDetail = Loadable(
  lazy(() => import('./pages/company/SupplierPartDetail'))
);

const ManufacturerPartDetail = Loadable(
  lazy(() => import('./pages/company/ManufacturerPartDetail'))
);

const CategoryDetail = Loadable(
  lazy(() => import('./pages/part/CategoryDetail'))
);
const PartDetail = Loadable(lazy(() => import('./pages/part/PartDetail')));

const LocationDetail = Loadable(
  lazy(() => import('./pages/stock/LocationDetail'))
);

const StockDetail = Loadable(lazy(() => import('./pages/stock/StockDetail')));

const BuildIndex = Loadable(lazy(() => import('./pages/build/BuildIndex')));

const BuildDetail = Loadable(lazy(() => import('./pages/build/BuildDetail')));

const PurchasingIndex = Loadable(
  lazy(() => import('./pages/purchasing/PurchasingIndex'))
);

const PurchaseOrderDetail = Loadable(
  lazy(() => import('./pages/purchasing/PurchaseOrderDetail'))
);

const SalesIndex = Loadable(lazy(() => import('./pages/sales/SalesIndex')));

const SalesOrderDetail = Loadable(
  lazy(() => import('./pages/sales/SalesOrderDetail'))
);

const SalesOrderShipmentDetail = Loadable(
  lazy(() => import('./pages/sales/SalesOrderShipmentDetail'))
);

const ReturnOrderDetail = Loadable(
  lazy(() => import('./pages/sales/ReturnOrderDetail'))
);

const Scan = Loadable(lazy(() => import('./pages/Index/Scan')));

const ErrorPage = Loadable(lazy(() => import('./pages/ErrorPage')));

const Notifications = Loadable(lazy(() => import('./pages/Notifications')));

const UserSettings = Loadable(
  lazy(() => import('./pages/Index/Settings/UserSettings'))
);

const SystemSettings = Loadable(
  lazy(() => import('./pages/Index/Settings/SystemSettings'))
);

const AdminCenter = Loadable(
  lazy(() => import('./pages/Index/Settings/AdminCenter/Index'))
);

// Core object
const CoreIndex = Loadable(lazy(() => import('./pages/core/CoreIndex')));
const UserDetail = Loadable(lazy(() => import('./pages/core/UserDetail')));
const GroupDetail = Loadable(lazy(() => import('./pages/core/GroupDetail')));

const NotFound = Loadable(lazy(() => import('./components/errors/NotFound')));

// Auth
const Login = Loadable(lazy(() => import('./pages/Auth/Login')));
const LoggedIn = Loadable(
  lazy(() => import('./pages/Auth/LoggedIn')),
  true,
  true
);
const Logout = Loadable(lazy(() => import('./pages/Auth/Logout')));
const Register = Loadable(lazy(() => import('./pages/Auth/Register')));
const Mfa = Loadable(lazy(() => import('./pages/Auth/MFA')));
const MfaSetup = Loadable(lazy(() => import('./pages/Auth/MFASetup')));
const ChangePassword = Loadable(
  lazy(() => import('./pages/Auth/ChangePassword'))
);
const Reset = Loadable(lazy(() => import('./pages/Auth/Reset')));
const ResetPassword = Loadable(
  lazy(() => import('./pages/Auth/ResetPassword'))
);
const VerifyEmail = Loadable(
  lazy(() => import('./pages/Auth/VerifyEmail')),
  true,
  true
);

// Create root route
const rootRoute = createRootRoute({
  component: Outlet,
  errorComponent: ErrorPage,
  notFoundComponent: NotFound
});

// Main layout route
const mainLayoutRoute = createRoute({
  getParentRoute: () => rootRoute,
  id: 'mainLayout',
  component: LayoutComponent
});

// Home routes
const homeIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/',
  component: Home
});

const homeRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/home',
  component: Home
});

// Notifications - with splat for sub-routes
const notificationsRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/notifications',
  component: Notifications
});

const notificationsSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/notifications/$',
  component: Notifications
});

// Scan
const scanRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/scan',
  component: Scan
});

// Settings routes
const settingsIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/settings',
  beforeLoad: async () => {
    throw redirect({ to: '/settings/admin', replace: true });
  }
});

const settingsAdminRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/settings/admin',
  component: AdminCenter
});

const settingsAdminSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/settings/admin/$',
  component: AdminCenter
});

const settingsSystemRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/settings/system',
  component: SystemSettings
});

const settingsSystemSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/settings/system/$',
  component: SystemSettings
});

const settingsUserRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/settings/user',
  component: UserSettings
});

const settingsUserSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/settings/user/$',
  component: UserSettings
});

// Part routes
const partIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/part',
  beforeLoad: async () => {
    throw redirect({ to: '/part/category', replace: true });
  }
});

const partCategoryIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/part/category',
  component: CategoryDetail
});

const partCategoryRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/part/category/$id',
  component: CategoryDetail
});

const partCategorySplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/part/category/$id/$',
  component: CategoryDetail
});

const partDetailRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/part/$id',
  component: PartDetail
});

const partDetailSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/part/$id/$',
  component: PartDetail
});

// Stock routes
const stockIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/stock',
  beforeLoad: async () => {
    throw redirect({ to: '/stock/location', replace: true });
  }
});

const stockLocationIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/stock/location',
  component: LocationDetail
});

const stockLocationRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/stock/location/$id',
  component: LocationDetail
});

const stockLocationSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/stock/location/$id/$',
  component: LocationDetail
});

const stockItemRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/stock/item/$id',
  component: StockDetail
});

const stockItemSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/stock/item/$id/$',
  component: StockDetail
});

// Manufacturing routes
const manufacturingIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/manufacturing',
  beforeLoad: async () => {
    throw redirect({ to: '/manufacturing/index', replace: true });
  }
});

const manufacturingBuildIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/manufacturing/index',
  component: BuildIndex
});

const manufacturingBuildIndexSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/manufacturing/index/$',
  component: BuildIndex
});

const manufacturingBuildOrderRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/manufacturing/build-order/$id',
  component: BuildDetail
});

const manufacturingBuildOrderSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/manufacturing/build-order/$id/$',
  component: BuildDetail
});

// Purchasing routes
const purchasingIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing',
  beforeLoad: async () => {
    throw redirect({ to: '/purchasing/index', replace: true });
  }
});

const purchasingMainIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/index',
  component: PurchasingIndex
});

const purchasingMainIndexSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/index/$',
  component: PurchasingIndex
});

const purchasingOrderRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/purchase-order/$id',
  component: PurchaseOrderDetail
});

const purchasingOrderSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/purchase-order/$id/$',
  component: PurchaseOrderDetail
});

const purchasingSupplierRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/supplier/$id',
  component: SupplierDetail
});

const purchasingSupplierSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/supplier/$id/$',
  component: SupplierDetail
});

const purchasingSupplierPartRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/supplier-part/$id',
  component: SupplierPartDetail
});

const purchasingSupplierPartSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/supplier-part/$id/$',
  component: SupplierPartDetail
});

const purchasingManufacturerRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/manufacturer/$id',
  component: ManufacturerDetail
});

const purchasingManufacturerSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/manufacturer/$id/$',
  component: ManufacturerDetail
});

const purchasingManufacturerPartRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/manufacturer-part/$id',
  component: ManufacturerPartDetail
});

const purchasingManufacturerPartSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/manufacturer-part/$id/$',
  component: ManufacturerPartDetail
});

// Company routes
const companyRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/company/$id',
  component: CompanyDetail
});

const companySplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/company/$id/$',
  component: CompanyDetail
});

// Sales routes
const salesIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales',
  beforeLoad: async () => {
    throw redirect({ to: '/sales/index', replace: true });
  }
});

const salesMainIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales/index',
  component: SalesIndex
});

const salesMainIndexSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales/index/$',
  component: SalesIndex
});

const salesOrderRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales/sales-order/$id',
  component: SalesOrderDetail
});

const salesOrderSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales/sales-order/$id/$',
  component: SalesOrderDetail
});

const salesShipmentRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales/shipment/$id',
  component: SalesOrderShipmentDetail
});

const salesShipmentSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales/shipment/$id/$',
  component: SalesOrderShipmentDetail
});

const salesReturnOrderRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales/return-order/$id',
  component: ReturnOrderDetail
});

const salesReturnOrderSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales/return-order/$id/$',
  component: ReturnOrderDetail
});

const salesCustomerRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales/customer/$id',
  component: CustomerDetail
});

const salesCustomerSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales/customer/$id/$',
  component: CustomerDetail
});

// Core routes
const coreIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/core',
  beforeLoad: async () => {
    throw redirect({ to: '/core/index', replace: true });
  }
});

const coreMainIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/core/index',
  component: CoreIndex
});

const coreMainIndexSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/core/index/$',
  component: CoreIndex
});

const coreUserRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/core/user/$id',
  component: UserDetail
});

const coreUserSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/core/user/$id/$',
  component: UserDetail
});

const coreGroupRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/core/group/$id',
  component: GroupDetail
});

const coreGroupSplatRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/core/group/$id/$',
  component: GroupDetail
});

// Login layout route
const loginLayoutRoute = createRoute({
  getParentRoute: () => rootRoute,
  id: 'authLayout',
  component: LoginLayoutComponent
});

// Auth routes
const loginRoute = createRoute({
  getParentRoute: () => loginLayoutRoute,
  path: '/login',
  component: Login
});

const loggedInRoute = createRoute({
  getParentRoute: () => loginLayoutRoute,
  path: '/logged-in',
  component: LoggedIn
});

const logoutRoute = createRoute({
  getParentRoute: () => loginLayoutRoute,
  path: '/logout',
  component: Logout
});

const registerRoute = createRoute({
  getParentRoute: () => loginLayoutRoute,
  path: '/register',
  component: Register
});

const mfaRoute = createRoute({
  getParentRoute: () => loginLayoutRoute,
  path: '/mfa',
  component: Mfa
});

const mfaSetupRoute = createRoute({
  getParentRoute: () => loginLayoutRoute,
  path: '/mfa-setup',
  component: MfaSetup
});

const changePasswordRoute = createRoute({
  getParentRoute: () => loginLayoutRoute,
  path: '/change-password',
  component: ChangePassword
});

const resetPasswordRoute = createRoute({
  getParentRoute: () => loginLayoutRoute,
  path: '/reset-password',
  component: Reset
});

const setPasswordRoute = createRoute({
  getParentRoute: () => loginLayoutRoute,
  path: '/set-password/$key',
  component: ResetPassword
});

const verifyEmailRoute = createRoute({
  getParentRoute: () => loginLayoutRoute,
  path: '/verify-email/$key',
  component: VerifyEmail
});

// Create route tree
const routeTree = rootRoute.addChildren([
  mainLayoutRoute.addChildren([
    homeIndexRoute,
    homeRoute,
    notificationsRoute,
    notificationsSplatRoute,
    scanRoute,
    settingsIndexRoute,
    settingsAdminRoute,
    settingsAdminSplatRoute,
    settingsSystemRoute,
    settingsSystemSplatRoute,
    settingsUserRoute,
    settingsUserSplatRoute,
    partIndexRoute,
    partCategoryIndexRoute,
    partCategoryRoute,
    partCategorySplatRoute,
    partDetailRoute,
    partDetailSplatRoute,
    stockIndexRoute,
    stockLocationIndexRoute,
    stockLocationRoute,
    stockLocationSplatRoute,
    stockItemRoute,
    stockItemSplatRoute,
    manufacturingIndexRoute,
    manufacturingBuildIndexRoute,
    manufacturingBuildIndexSplatRoute,
    manufacturingBuildOrderRoute,
    manufacturingBuildOrderSplatRoute,
    purchasingIndexRoute,
    purchasingMainIndexRoute,
    purchasingMainIndexSplatRoute,
    purchasingOrderRoute,
    purchasingOrderSplatRoute,
    purchasingSupplierRoute,
    purchasingSupplierSplatRoute,
    purchasingSupplierPartRoute,
    purchasingSupplierPartSplatRoute,
    purchasingManufacturerRoute,
    purchasingManufacturerSplatRoute,
    purchasingManufacturerPartRoute,
    purchasingManufacturerPartSplatRoute,
    companyRoute,
    companySplatRoute,
    salesIndexRoute,
    salesMainIndexRoute,
    salesMainIndexSplatRoute,
    salesOrderRoute,
    salesOrderSplatRoute,
    salesShipmentRoute,
    salesShipmentSplatRoute,
    salesReturnOrderRoute,
    salesReturnOrderSplatRoute,
    salesCustomerRoute,
    salesCustomerSplatRoute,
    coreIndexRoute,
    coreMainIndexRoute,
    coreMainIndexSplatRoute,
    coreUserRoute,
    coreUserSplatRoute,
    coreGroupRoute,
    coreGroupSplatRoute
  ]),
  loginLayoutRoute.addChildren([
    loginRoute,
    loggedInRoute,
    logoutRoute,
    registerRoute,
    mfaRoute,
    mfaSetupRoute,
    changePasswordRoute,
    resetPasswordRoute,
    setPasswordRoute,
    verifyEmailRoute
  ])
]);

// Create router
export const router = createRouter({
  routeTree,
  defaultErrorComponent: ErrorPage,
  defaultNotFoundComponent: NotFound
});

// Register router type for type safety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
}
