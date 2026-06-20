export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
}

export interface Datasource {
  id: string;
  user_id: string;
  name: string;
  type: string;
  config: string;
  description: string;
  created_at: string;
}

export interface QueryResult {
  id: string;
  user_id: string;
  datasource_id: string | null;
  question: string;
  sql_generated: string;
  python_generated: string;
  result_json: string;
  chart_config: string;
  summary: string;
  execution_time: number;
  status: string;
  created_at: string;
}

export interface Skill {
  id: string;
  user_id: string;
  name: string;
  description: string;
  prompt_template: string;
  parameters: string;
  is_public: boolean;
  category: string;
  created_at: string;
  updated_at: string;
}

export interface Dashboard {
  id: string;
  user_id: string;
  name: string;
  description: string;
  layout: string;
  created_at: string;
  updated_at: string;
}

export interface DashboardWidget {
  id: string;
  dashboard_id: string;
  title: string;
  type: string;
  config: string;
  position_x: number;
  position_y: number;
  width: number;
  height: number;
}

export interface Report {
  id: string;
  user_id: string;
  title: string;
  description: string;
  html_content: string;
  query_ids: string;
  share_token: string;
  created_at: string;
  updated_at: string;
}

export interface ChatEvent {
  type: "status" | "plan" | "sql" | "result" | "analysis" | "error" | "chart";
  content: string;
  metadata?: string;
}

export interface Settings {
  gemini_api_key: string;
  ollama_base_url: string;
  ollama_model: string;
}
