import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  message: "",
  variant: "success", // 支持 success, danger, warning 等
  show: false,
};

export const toastSlice = createSlice({
  name: "toast",
  initialState,
  reducers: {
    showToast: (state, action) => {
      state.message = action.payload.message;
      state.variant = action.payload.variant || "success";
      state.show = true;
    },
    hideToast: (state) => {
      state.show = false;
    },
  },
});

export const { showToast, hideToast } = toastSlice.actions;
export default toastSlice.reducer;
