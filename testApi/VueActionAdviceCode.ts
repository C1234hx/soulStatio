// 1. 数据模型定义
// src/types/actionAdvice.ts
export interface ActionAdvice {
  id: string;
  emotion_direction: number; // 0-正向，1-普通，2-负向
  content: string;
  is_active: boolean;
  created_at: string;
}

// 2. API服务
// src/services/actionAdviceService.ts
import axios from 'axios';
import type { ActionAdvice } from '../types/actionAdvice';

// 创建axios实例
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

export const actionAdviceService = {
  // 获取所有行动建议
  async getAllActionAdvices(): Promise<ActionAdvice[]> {
    try {
      const response = await apiClient.get('/action-advice/');
      return response.data;
    } catch (error) {
      console.error('获取行动建议失败:', error);
      throw error;
    }
  }
};

// 3. Vue组件示例
// src/components/ActionAdviceList.vue
<template>
  <div class="action-advice-list">
    <h2>行动建议列表</h2>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading">加载中...</div>
    
    <!-- 错误提示 -->
    <div v-else-if="error" class="error">
      <p>获取数据失败: {{ error }}</p>
      <button @click="fetchActionAdvices">重试</button>
    </div>
    
    <!-- 数据列表 -->
    <table v-else-if="actionAdvices.length > 0" class="advice-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>情绪向</th>
          <th>内容</th>
          <th>启用状态</th>
          <th>创建时间</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="advice in actionAdvices" :key="advice.id">
          <td>{{ advice.id }}</td>
          <td>{{ getEmotionText(advice.emotion_direction) }}</td>
          <td>{{ advice.content }}</td>
          <td>{{ advice.is_active ? '启用' : '禁用' }}</td>
          <td>{{ formatDate(advice.created_at) }}</td>
        </tr>
      </tbody>
    </table>
    
    <!-- 空数据提示 -->
    <div v-else class="empty">暂无行动建议数据</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { actionAdviceService } from '../services/actionAdviceService';
import type { ActionAdvice } from '../types/actionAdvice';

// 响应式数据
const actionAdvices = ref<ActionAdvice[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

// 获取行动建议数据
const fetchActionAdvices = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    actionAdvices.value = await actionAdviceService.getAllActionAdvices();
  } catch (err) {
    error.value = err instanceof Error ? err.message : '未知错误';
  } finally {
    loading.value = false;
  }
};

// 将数字情绪向转换为文字
const getEmotionText = (direction: number): string => {
  switch (direction) {
    case 0: return '正向';
    case 1: return '普通';
    case 2: return '负向';
    default: return '未知';
  }
};

// 格式化日期
const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN');
};

// 组件挂载时获取数据
onMounted(() => {
  fetchActionAdvices();
});
</script>

<style scoped>
.action-advice-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.loading, .error, .empty {
  text-align: center;
  padding: 20px;
  font-size: 16px;
}

.error {
  color: #ff4444;
}

.error button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.error button:hover {
  background-color: #1976d2;
}

.advice-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.advice-table th, .advice-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.advice-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.advice-table tr:hover {
  background-color: #f5f5f5;
}
</style>