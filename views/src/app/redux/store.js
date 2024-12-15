import { configureStore } from "@reduxjs/toolkit";
import userReducer from './slices/userSlice';
import cartReducer from './slices/cartSlice';
import loadingReducer from './slices/loadingSlice';
import toastReducer from "./slices/toastSlice";
import { persistStore, persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage"; // 使用 localStorage
import { combineReducers } from "redux";

const persistConfig = {
  key: "root",
  storage,
};

const rootReducer = combineReducers({
  user: userReducer,
  cart: cartReducer,
  loading: loadingReducer,
  toast: toastReducer,
});

const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ["persist/PERSIST", "persist/REHYDRATE"],
      },
    }),
});

export const persistor = persistStore(store);
