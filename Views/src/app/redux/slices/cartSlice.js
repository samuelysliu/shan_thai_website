import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  items: [], // 購物車商品列表
};

export const cartSlice = createSlice({
  name: "cart",
  initialState,
  reducers: {
    addToCart: (state, action) => {
      const product = action.payload;
      const existingItem = state.items.find((item) => item.pid === product.pid);
      if (existingItem) {
        existingItem.quantity += 1;
      } else {
        state.items.push({ ...product, quantity: 1 });
      }
    },
    updateQuantity: (state, action) => {
      const { pid, quantity } = action.payload;
      const existingItem = state.items.find((item) => item.pid === pid);
      if (existingItem) {
        existingItem.quantity += quantity;
        if (existingItem.quantity < 1) {
          state.items = state.items.filter((item) => item.pid !== pid);
        }
      }
    },
    removeFromCart: (state, action) => {
      state.items = state.items.filter((item) => item.pid !== action.payload);
    },
  },
});

export const { addToCart, updateQuantity, removeFromCart } = cartSlice.actions;
export default cartSlice.reducer;
