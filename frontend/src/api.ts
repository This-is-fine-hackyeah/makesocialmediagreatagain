import axios from 'axios';

export enum TweetState {
  initial = 'initial',
  accepted = 'accepted',
  declined = 'declined'
}

const apiUrl = 'http://localhost/api/v1'
function formatDate(date: Date) {
  return date.toISOString().slice(0, 19);
}

export const api = {
  async getLatestTweets(date: Date) {
    let params = {};

    if (date) {
      params = {
        from_date: formatDate(date),
      }
    }
    
    const resp = await axios.get(`${apiUrl}/get-recent-tweets`, { params });
    return resp.data
  },
  
  async changeState(id: string, state: TweetState) {
    await axios.post(`${apiUrl}/change`, {
      'status': state,
      'id': id
    });
  },

  async getStatistics() {
    const resp = await axios.get(`${apiUrl}/get-statistics`);
    console.log(resp)
    return resp.data
  }
};
