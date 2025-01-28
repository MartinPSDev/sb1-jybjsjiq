export interface SearchParams {
  destination: string;
  startDate: string;
  endDate: string;
  guests: number;
  budget: number;
}

export interface SearchResult {
  site: string;
  price: number;
  link: string;
  description: string;
  rating?: number;
  imageUrl?: string;
}

export interface ProcessedResults {
  bestOption: SearchResult;
  allOptions: SearchResult[];
  totalFound: number;
}