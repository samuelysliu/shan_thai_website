import { Provider } from 'react-redux';
import { store, persistor } from "./redux/store";
import '../styles/globals.css';
import { PersistGate } from "redux-persist/integration/react";


function MyApp({ Component, pageProps }) {
  

  return (
    <Provider store={store}>
      <PersistGate loading={<Loader />} persistor={persistor}>
        <Loader />
        <AlertToast />
        <Component {...pageProps} />
      </PersistGate>
    </Provider>
  );
}

export default MyApp;
