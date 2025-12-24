<template>
  <div class="course-list-page">
    <!-- 페이지 헤더 -->
    <section class="page-header">
      <div class="container">
        <h2>강좌 찾기</h2>
        <div class="search-wrapper">
          <input 
            type="text" 
            placeholder="강좌명, 대학명, 교수명을 검색해보세요"
            v-model="searchQuery"
            @keyup.enter="triggerSearch"
          >
          <button @click="triggerSearch">검색</button>
        </div>
      </div>
    </section>

    <div class="container layout-container">
      <!-- 사이드바 필터 -->
      <aside class="sidebar">
        <div class="filter-group">
          <h3>분야별</h3>
          <ul>
            <li v-for="cat in categories" :key="cat">
              <label>
                <input type="checkbox" :value="cat" v-model="selectedCategories">
                {{ cat }}
              </label>
            </li>
          </ul>
        </div>
        
        <div class="filter-group">
          <h3>강좌 상태</h3>
          <ul>
            <li v-for="stat in statusOptions" :key="stat">
              <label>
                <input type="checkbox" :value="stat" v-model="selectedStatuses">
                {{ stat }}
              </label>
            </li>
          </ul>
        </div>
      </aside>

      <!-- 메인 컨텐츠 -->
      <main class="content">
        
        <!-- Case 1: 검색 전 (전체 목록) -->
        <div v-if="!isSearched">
          <div class="list-control">
            <span class="total-count">총 <strong>{{ totalCount }}</strong>개의 강좌</span>
            <div class="sort-options">
              <select v-model="sortBy" @change="loadInitialCourses">
                <option value="latest">최신순</option>
                <option value="-average_rating">평점순</option>
              </select>
            </div>
          </div>

          <div v-if="isLoading" class="loading-state"><p>강좌 목록을 불러오는 중...</p></div>
          <div v-else-if="courses.length > 0" class="course-grid">
            <CourseCard v-for="course in courses" :key="course.id" v-bind="course" />
          </div>
          <div v-else class="empty-state"><p>강좌가 없습니다.</p></div>
          
          <!-- 전체 목록 페이지네이션 (간단 구현) -->
          <div class="pagination" v-if="courses.length > 0">
             <!-- 실제로는 API 페이지네이션 연동 필요하지만, 여기서는 생략하고 더보기 버튼 등으로 대체 가능 -->
          </div>
        </div>

        <!-- Case 2: 검색 후 (두 개의 섹션) -->
        <div v-else class="search-results">
          
          <button class="btn-back-all" @click="clearSearch">← 전체 목록으로 돌아가기</button>

          <!-- 섹션 1: AI 의미 기반 검색 -->
          <section class="result-section ai-section">
            <div class="section-head">
              <h3>🤖 AI 의미 기반 검색 결과</h3>
              <span class="count-badge">{{ semanticAllData.length }}건</span>
            </div>
            
            <div v-if="semanticLoading" class="loading-state small"><p>AI 분석 중...</p></div>
            <div v-else-if="semanticDisplayData.length > 0">
              <div class="course-grid">
                <CourseCard v-for="course in semanticDisplayData" :key="course.id" v-bind="course" />
              </div>
              <!-- Client-side Pagination -->
              <div class="pagination" v-if="semanticAllData.length > 3">
                <button class="page-btn" :disabled="semanticPage === 1" @click="semanticPage--">&lt;</button>
                <span class="page-info">{{ semanticPage }} / {{ Math.ceil(semanticAllData.length / 3) }}</span>
                <button class="page-btn" :disabled="semanticPage * 3 >= semanticAllData.length" @click="semanticPage++">&gt;</button>
              </div>
            </div>
            <div v-else class="empty-state small"><p>AI 검색 결과가 없습니다.</p></div>
          </section>

          <!-- 섹션 2: 키워드 검색 -->
          <section class="result-section keyword-section">
            <div class="section-head">
              <h3>🔍 키워드 검색 결과</h3>
              <span class="count-badge">{{ totalKeywordCount }}건</span>
            </div>

            <div v-if="keywordLoading" class="loading-state small"><p>검색 중...</p></div>
            <div v-else-if="keywordCourses.length > 0">
              <div class="course-grid">
                <CourseCard v-for="course in keywordCourses" :key="course.id" v-bind="course" />
              </div>
              <!-- Server-side Pagination -->
              <div class="pagination" v-if="totalKeywordCount > 3">
                <button class="page-btn" :disabled="keywordPage === 1" @click="changeKeywordPage(keywordPage - 1)">&lt;</button>
                <span class="page-info">{{ keywordPage }} / {{ Math.ceil(totalKeywordCount / 3) }}</span>
                <button class="page-btn" :disabled="keywordPage * 3 >= totalKeywordCount" @click="changeKeywordPage(keywordPage + 1)">&gt;</button>
              </div>
            </div>
            <div v-else class="empty-state small"><p>키워드 검색 결과가 없습니다.</p></div>
          </section>

        </div>

      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import CourseCard from '@/components/common/CourseCard.vue';
import { getCourseList, searchSemanticCourses } from '@/api/courses';

const searchQuery = ref('');
const selectedCategories = ref([]);
const selectedStatuses = ref([]);
const sortBy = ref('-average_rating');

// 상태 관리
const isSearched = ref(false);
const isLoading = ref(false);

// 전체 목록 (초기)
const courses = ref([]);
const totalCount = ref(0);

// 검색 결과 데이터
const keywordCourses = ref([]);
const totalKeywordCount = ref(0);
const keywordPage = ref(1);
const keywordLoading = ref(false);

const semanticAllData = ref([]); // 전체 데이터 (Client Pagination)
const semanticPage = ref(1);
const semanticLoading = ref(false);

const categories = [
  '인문', '사회', '교육', '공학', '자연', '의약', '예체능', '융·복합', '기타'
];
const statusOptions = ['접수중', '개강임박', '상시', '종료'];

// --- 초기 로딩 ---
const loadInitialCourses = async () => {
  isLoading.value = true;
  try {
    const { data } = await getCourseList({
      ordering: sortBy.value,
      page_size: 9
    });
    courses.value = data.results || [];
    totalCount.value = data.count || 0;
  } catch (error) {
    console.error("초기 로딩 실패:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadInitialCourses();
});

// --- 검색 트리거 ---
const triggerSearch = () => {
  const query = searchQuery.value.trim();
  if (!query) {
    alert("검색어를 입력해주세요.");
    return;
  }
  isSearched.value = true;
  
  // 상태 초기화
  keywordPage.value = 1;
  semanticPage.value = 1;
  
  // 두 검색 동시에 실행
  fetchKeywordSearch(query);
  fetchSemanticSearch(query);
};

const clearSearch = () => {
  isSearched.value = false;
  searchQuery.value = '';
  loadInitialCourses();
};

// --- 1. 키워드 검색 (Server Pagination) ---
const fetchKeywordSearch = async (query) => {
  keywordLoading.value = true;
  try {
    const { data } = await getCourseList({
      search: query,
      page: keywordPage.value,
      page_size: 3
    });
    keywordCourses.value = data.results || [];
    totalKeywordCount.value = data.count || 0;
  } catch (error) {
    console.error("키워드 검색 실패:", error);
    keywordCourses.value = [];
  } finally {
    keywordLoading.value = false;
  }
};

const changeKeywordPage = (newPage) => {
  if (newPage < 1) return;
  keywordPage.value = newPage;
  fetchKeywordSearch(searchQuery.value);
};

// --- 2. 시맨틱 검색 (Client Pagination) ---
const fetchSemanticSearch = async (query) => {
  semanticLoading.value = true;
  try {
    const { data } = await searchSemanticCourses(query);
    semanticAllData.value = data || [];
  } catch (error) {
    console.error("AI 검색 실패:", error);
    semanticAllData.value = [];
  } finally {
    semanticLoading.value = false;
  }
};

// 시맨틱 데이터 슬라이싱
const semanticDisplayData = computed(() => {
  const start = (semanticPage.value - 1) * 3;
  return semanticAllData.value.slice(start, start + 3);
});

</script>

<style scoped>
.page-header { background: var(--bg-light); padding: 40px 0; margin-bottom: 40px; }
.page-header h2 { text-align: center; margin-bottom: 20px; font-size: 32px; font-weight: 700; }
.search-wrapper { max-width: 600px; margin: 0 auto; display: flex; gap: 10px; }
.search-wrapper input { flex: 1; padding: 15px 20px; border: 1px solid var(--border); border-radius: 4px; font-size: 16px; outline: none; }
.search-wrapper input:focus { border-color: var(--primary); }
.search-wrapper button { padding: 0 30px; background: var(--primary); color: white; border: none; border-radius: 4px; font-weight: 600; cursor: pointer; transition: 0.3s; font-size: 16px; }
.search-wrapper button:hover { background: var(--primary-dark); }

.layout-container { display: flex; gap: 40px; margin-bottom: 80px; }

/* Sidebar */
.sidebar { width: 220px; flex-shrink: 0; }
.filter-group { margin-bottom: 30px; }
.filter-group h3 { font-size: 18px; font-weight: 700; margin-bottom: 15px; border-bottom: 2px solid var(--text-main); padding-bottom: 10px; }
.filter-group ul li { margin-bottom: 10px; }
.filter-group label { cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: 15px; color: var(--text-sub); }
.filter-group input[type="checkbox"] { width: 16px; height: 16px; accent-color: var(--primary); }
.filter-group label:hover { color: var(--primary); }

/* Main Content */
.content { flex: 1; }
.list-control { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.total-count { font-size: 15px; color: var(--text-sub); }
.total-count strong { color: var(--primary); }
.sort-options select { padding: 8px 12px; border: 1px solid var(--border); border-radius: 4px; outline: none; font-size: 14px; cursor: pointer; }

/* Grid & Layout */
.course-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 20px; }

/* Search Results Sections */
.result-section { margin-bottom: 50px; }
.section-head { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid #eee; padding-bottom: 10px; }
.section-head h3 { font-size: 20px; font-weight: 800; margin: 0; color: var(--text-main); }
.ai-section .section-head h3 { color: var(--primary); }
.count-badge { background: #eee; padding: 2px 8px; border-radius: 10px; font-size: 12px; font-weight: 700; }

.btn-back-all { background: none; border: none; color: #666; cursor: pointer; margin-bottom: 20px; font-weight: 600; text-decoration: underline; }

/* Loading & Empty State */
.loading-state, .empty-state { text-align: center; padding: 60px 20px; color: var(--text-sub); font-size: 16px; }
.loading-state.small, .empty-state.small { padding: 30px; background: #f9f9f9; border-radius: 8px; margin-bottom: 20px; }
.loading-state p::before { content: '⏳ '; }
.empty-state p::before { content: '📭 '; }

/* Pagination */
.pagination { display: flex; justify-content: center; gap: 10px; align-items: center; margin-top: 10px; }
.page-btn { width: 32px; height: 32px; border: 1px solid var(--border); background: white; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.page-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.page-info { font-size: 14px; font-weight: 600; color: #666; }
</style>
