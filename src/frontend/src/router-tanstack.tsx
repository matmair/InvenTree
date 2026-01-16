import { lazy } from 'react';
import {
  createRootRoute,
  createRoute,
  createRouter,
  Navigate,
  Outlet
} from '@tanstack/react-router';

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

const NotFound = Loadable(
  lazy(() => import('./components/errors/NotFound'))
);

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

// Root route
const rootRoute = createRootRoute({
  component: Outlet,
  errorComponent: ErrorPage,
  notFoundComponent: NotFound
});

// Main layout route
const mainLayoutRoute = createRoute({
  getParentRoute: () => rootRoute,
  id: 'main-layout',
  component: LayoutComponent
});

// Auth layout route
const authLayoutRoute = createRoute({
  getParentRoute: () => rootRoute,
  id: 'auth-layout',
  component: LoginLayoutComponent
});

// Main app routes
const indexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/',
  component: Home
});

const homeRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/home',
  component: Home
});

const notificationsRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/notifications',
  component: Notifications
});

const scanRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/scan',
  component: Scan
});

// Settings routes
const settingsIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/settings',
  component: () => <Navigate to="/settings/admin" />
});

const settingsAdminRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/settings/admin',
  component: AdminCenter
});

const settingsSystemRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/settings/system',
  component: SystemSettings
});

const settingsUserRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/settings/user',
  component: UserSettings
});

// Part routes
const partIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/part',
  component: () => <Navigate to="/part/category/index" />
});

const partCategoryRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/part/category/$id',
  component: CategoryDetail
});

const partCategoryIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/part/category/index',
  component: CategoryDetail
});

const partDetailRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/part/$id',
  component: PartDetail
});

// Stock routes
const stockIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/stock',
  component: () => <Navigate to="/stock/location/index" />
});

const stockLocationRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/stock/location/$id',
  component: LocationDetail
});

const stockLocationIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/stock/location/index',
  component: LocationDetail
});

const stockItemRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/stock/item/$id',
  component: StockDetail
});

// Manufacturing routes
const manufacturingIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/manufacturing',
  component: () => <Navigate to="/manufacturing/index" />
});

const manufacturingBuildIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/manufacturing/index',
  component: BuildIndex
});

const manufacturingBuildOrderRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/manufacturing/build-order/$id',
  component: BuildDetail
});

// Purchasing routes
const purchasingIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing',
  component: () => <Navigate to="/purchasing/index" />
});

const purchasingListRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/index',
  component: PurchasingIndex
});

const purchaseOrderRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/purchase-order/$id',
  component: PurchaseOrderDetail
});

const supplierRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/supplier/$id',
  component: SupplierDetail
});

const supplierPartRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/supplier-part/$id',
  component: SupplierPartDetail
});

const manufacturerRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/manufacturer/$id',
  component: ManufacturerDetail
});

const manufacturerPartRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/purchasing/manufacturer-part/$id',
  component: ManufacturerPartDetail
});

const companyRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/company/$id',
  component: CompanyDetail
});

// Sales routes
const salesIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales',
  component: () => <Navigate to="/sales/index" />
});

const salesListRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales/index',
  component: SalesIndex
});

const salesOrderRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales/sales-order/$id',
  component: SalesOrderDetail
});

const salesShipmentRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales/shipment/$id',
  component: SalesOrderShipmentDetail
});

const returnOrderRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales/return-order/$id',
  component: ReturnOrderDetail
});

const customerRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/sales/customer/$id',
  component: CustomerDetail
});

// Core routes
const coreIndexRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/core',
  component: () => <Navigate to="/core/index" />
});

const coreListRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/core/index',
  component: CoreIndex
});

const coreUserRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/core/user/$id',
  component: UserDetail
});

const coreGroupRoute = createRoute({
  getParentRoute: () => mainLayoutRoute,
  path: '/core/group/$id',
  component: GroupDetail
});

// Auth routes
const loginRoute = createRoute({
  getParentRoute: () => authLayoutRoute,
  path: '/login',
  component: Login
});

const loggedInRoute = createRoute({
  getParentRoute: () => authLayoutRoute,
  path: '/logged-in',
  component: LoggedIn
});

const logoutRoute = createRoute({
  getParentRoute: () => authLayoutRoute,
  path: '/logout',
  component: Logout
});

const registerRoute = createRoute({
  getParentRoute: () => authLayoutRoute,
  path: '/register',
  component: Register
});

const mfaRoute = createRoute({
  getParentRoute: () => authLayoutRoute,
  path: '/mfa',
  component: Mfa
});

const mfaSetupRoute = createRoute({
  getParentRoute: () => authLayoutRoute,
  path: '/mfa-setup',
  component: MfaSetup
});

const changePasswordRoute = createRoute({
  getParentRoute: () => authLayoutRoute,
  path: '/change-password',
  component: ChangePassword
});

const resetPasswordRoute = createRoute({
  getParentRoute: () => authLayoutRoute,
  path: '/reset-password',
  component: Reset
});

const setPasswordRoute = createRoute({
  getParentRoute: () => authLayoutRoute,
  path: '/set-password',
  component: ResetPassword
});

const verifyEmailRoute = createRoute({
  getParentRoute: () => authLayoutRoute,
  path: '/verify-email/$key',
  component: VerifyEmail
});

// Create route tree
const routeTree = rootRoute.addChildren([
  mainLayoutRoute.addChildren([
    indexRoute,
    homeRoute,
    notificationsRoute,
    scanRoute,
    settingsIndexRoute,
    settingsAdminRoute,
    settingsSystemRoute,
    settingsUserRoute,
    partIndexRoute,
    partCategoryRoute,
    partCategoryIndexRoute,
    partDetailRoute,
    stockIndexRoute,
    stockLocationRoute,
    stockLocationIndexRoute,
    stockItemRoute,
    manufacturingIndexRoute,
    manufacturingBuildIndexRoute,
    manufacturingBuildOrderRoute,
    purchasingIndexRoute,
    purchasingListRoute,
    purchaseOrderRoute,
    supplierRoute,
    supplierPartRoute,
    manufacturerRoute,
    manufacturerPartRoute,
    companyRoute,
    salesIndexRoute,
    salesListRoute,
    salesOrderRoute,
    salesShipmentRoute,
    returnOrderRoute,
    customerRoute,
    coreIndexRoute,
    coreListRoute,
    coreUserRoute,
    coreGroupRoute
  ]),
  authLayoutRoute.addChildren([
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
  defaultPreload: 'intent'
});

// Register router for type safety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
}
