import { createApp } from 'vue'
import PrimeVue from "primevue/config";
import './sass/main.scss'
import App from './App.vue'
import 'primevue/resources/themes/aura-light-green/theme.css'
import router from './router/routes'
import ConfirmationService from 'primevue/confirmationservice';

const app = createApp(App)

app.use(router)
app.use(PrimeVue);
app.use(ConfirmationService);
app.mount('#app')