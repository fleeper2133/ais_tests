import { createApp } from 'vue'
import PrimeVue from "primevue/config";
import './sass/main.scss'
import App from './components/App.vue'
import 'primevue/resources/themes/aura-light-green/theme.css'
import router from './router/routes'
import ConfirmationService from 'primevue/confirmationservice';
import { createPinia } from 'pinia';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.bundle.js';

import './eventBus.ts';
import './settings.ts';

const pinia = createPinia();
const app = createApp(App)

app.use(router)
app.use(PrimeVue)
app.use(pinia)
app.use(ConfirmationService)
app.mount('#app')