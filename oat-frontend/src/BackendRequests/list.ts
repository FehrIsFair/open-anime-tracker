import engine from './base';
import { ListStatus, UserListItem } from '../Models/list';

export const fetchUserList = async (
  status?: ListStatus,
  sort?: string
): Promise<{ data: UserListItem[] }> => {
  const params: Record<string, string> = {};
  if (status) {
    params.status = status;
  }
  if (sort) {
    params.sort = sort;
  }
  const res = await engine.get('/list', { params });
  return res.data;
};

export const addToList = async (
  animeId: number,
  status?: ListStatus
): Promise<{ message: string; data: any }> => {
  const payload: { anime_id: number; status?: ListStatus } = { anime_id: animeId };
  if (status) {
    payload.status = status;
  }
  const res = await engine.post('/list', payload);
  return res.data;
};

export const updateListStatus = async (
  animeId: number,
  status: ListStatus
): Promise<{ message: string; data: any }> => {
  const res = await engine.patch(`/list/${animeId}`, { status });
  return res.data;
};

export const removeFromList = async (
  animeId: number
): Promise<{ message: string }> => {
  const res = await engine.delete(`/list/${animeId}`);
  return res.data;
};

export const fetchAnimeListStatus = async (
  animeId: number
): Promise<{ in_list: boolean; status: ListStatus | null; id?: number }> => {
  const res = await engine.get(`/list/anime/${animeId}`);
  return res.data;
};
