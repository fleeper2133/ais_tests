import axios from 'axios'
import { jwtDecode } from "jwt-decode";


class ApiClient {
  baseURL: string
  headers: any
  client: any
  constructor({ baseURL, headers }) {
    this.baseURL = baseURL;
    this.headers = headers;
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: this.headers,
    });
  }

  async get(path, { headers, queryParams }: any = {}) {
    const response = await this.client.get(path, {
      headers: { ...this.headers, ...headers },
      params: queryParams,
    });
    return response.data;
  }

  async post(path, body, { headers, queryParams }: any = {}) {
    const response = await this.client.post(path, body, {
      headers: { ...this.headers, ...headers },
      params: queryParams,
    });
    return response.data;
  }

  async put(path, body, { headers, queryParams }: any = {}) {
    const response = await this.client.put(path, body, {
      headers: { ...this.headers, ...headers },
      params: queryParams,
    });
    return response.data;
  }

  async patch(path, body, { headers, queryParams }: any = {}) {
    const response = await this.client.patch(path, body, {
      headers: { ...this.headers, ...headers },
      params: queryParams,
    });
    return response.data;
  }

  async delete(path, { headers, queryParams }: any = {}) {
    const response = await this.client.delete(path, {
      headers: { ...this.headers, ...headers },
      params: queryParams,
    });
    return response.data;
  }



  async getCourses() {
    return this.get('/api/courses/');
  }

  async getCourseQuestions(id) {
    const url = `/api/user-courses/${id}/course_questions/`
    return this.get(url);
  }

  async getUserCourses() {
    return this.get('/api/user-courses/');
  }

  async setUserCourse(body) {
    return this.post('/api/user-courses/', body);
  }

  async startCourse(id, body) {
    const url = `/api/courses/${id}/start_course/`;
    return this.post(url, body);
  }

  async smartGenerate(body) {
    return this.post('api/user-check-skills/smart-generate-check/', body);
  }
  async getQuestionDetail(id) {
    const url = `/api/questions/${id}/detail/`
    return this.get(url);
  }

  async createAnswer(id, body) {
    const url = `/api/user-check-skills-questions/${id}/create_answer/`
    return this.post(url, body);
  }
  async endTraining(id) {
    const url = `api/user-check-skills/${id}/end_check/`
    return this.post(url);
  }


  

  async sendMail(body){
    return this.post(`/api/send-mail/`, body)
  }

  async login(body) {
    return this.post('/api/login/', body);
  }

  async logout(body) {
    return this.post('/api/logout/', body);
  }

  async registration(body) {
    return this.post('/api/registration/', body);
  }

}


export const tokenExpire = () => {
  const accessToken = localStorage.getItem('accessToken');
  if (!accessToken) {
    return false;
  }
  const payload = jwtDecode(accessToken);
  const expTime = payload.exp * 1000;
  const curTime = new Date().getTime();
  if (expTime - curTime <= 5000 || expTime - curTime < 0) {
    return true;
  }
  return false;
}

export const api = new ApiClient({
  baseURL: '',
  headers: {
    Accept: 'application/json',
  }
})

api.client.interceptors.request.use(async (config) => {
  const accessToken = localStorage.getItem('accessToken');
  if (accessToken && tokenExpire()) {
    try {
      const response = await axios.post('/api/token/refresh/', { refresh: localStorage.getItem('refreshToken') });
      const newAccessToken = response.data.access;
      const newRefreshToken = response.data.refresh;

      localStorage.setItem('accessToken', newAccessToken);
      localStorage.setItem('refreshToken', newRefreshToken);

      config.headers.Authorization = `Bearer ${newAccessToken}`;
    } catch (error) {
      console.error('Ошибка при обновлении токена:', error);
    }
  } else if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});