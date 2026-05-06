import { defineStore } from "pinia";

const fileListUrl = import.meta.env.VITE_API_URL + "/files/list";
export const useStore = defineStore("user", {
  state: () => ({
    fileList: [],
    isLoading: false,
    error: null as Error | null,
  }),

  actions: {
    async fetchFileList() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await fetch(fileListUrl);
        const data = await response.json();
        this.fileList = data;
      } catch (err) {
        this.error = err as Error;
      } finally {
        this.isLoading = false;
      }
    },
  },
});
