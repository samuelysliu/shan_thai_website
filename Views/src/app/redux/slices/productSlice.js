import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  products: [], // 初始化產品列表
};

const productSlice = createSlice({
  name: 'product',
  initialState,
  reducers: {
    setProducts: (state, action) => {
      state.products = action.payload; // 設置產品列表
    },
  },
});

export const { setProducts } = productSlice.actions; // 導出 actions
export default productSlice.reducer; // 導出 reducer
