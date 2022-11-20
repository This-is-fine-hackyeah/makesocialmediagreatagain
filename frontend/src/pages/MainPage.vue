<template>
  <div class="h-[100vh] row w-full page-wrapper">
    <q-scroll-area
      class="col column items-center mb-10"
      visible
    >
    <div v-for="tweet in tweets" :key="tweet.id" class="pt-10 row justify-center">
      <div class="w-[460px] px-3 py-10 bg-white" style="border-radius: 8px;">
        <Tweet :tweet-id="tweet.id" />
        <div class="px-3 py-3">
          <div class="row w-full justify-between">
            <div>
              Wiarygodność posta
            </div>
            <div :class="tweet.prediction > breakpoint ? 'good-alert' : 'bad-alert'" style="border-radius: 1000px; padding: 4px">
              {{ (tweet.prediction * 100).toFixed(0) + '%' }}
            </div>
          </div>
          <div class="py-3">
            <q-linear-progress rounded size="xl" :value="tweet.prediction" color="secondary" :class="tweet.prediction > breakpoint ? 'good-progress' : 'bad-progress'" />
          </div>
          <div class="row justify-between">
            <q-btn label="Odrzuć" :icon="matClose" class="button button-reject" rounded @click="updateState(tweet.id, TweetState.declined)" />
            <q-btn label="Akceptuj" :icon="matDone" class="button button-acccept" rounded @click="updateState(tweet.id, TweetState.accepted)" />
          </div>
        </div>
      </div>
    </div>
    </q-scroll-area>
    <div class="col-4 px-10 pt-10">
      <div class="py-6 bg-white" style="border: 1px solid #DFE0EB;border-radius: 8px;">
        <div class="text-xl text-bold px-6">Ostatnie 24h</div>
        <div class="row justify-between py-5" style="border-bottom: 1px solid #DFE0EB;">
          <div class="px-6" style="color: #252733;font-weight: 600;">Zaakceptowane</div>
          <div class="px-6" style="color: #06750A;">{{ accepted }}</div>
        </div>
        <div class="row justify-between py-5" style="border-bottom: 1px solid #DFE0EB;">
          <div class="px-6" style="color: #252733;font-weight: 600;">Odrzucone</div>
          <div class="px-6" style="color: #EA0000;">{{ declined }}</div>
        </div>
        <div class="row justify-between pt-5">
          <div class="px-6" style="color: #252733;font-weight: 600;">Oczekujące</div>
          <div class="px-6" style="color: #9FA2B4;">{{ initial }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { matDone, matClose } from '@quasar/extras/material-icons'
import Tweet from 'vue-tweet'
import { api, TweetState } from '@/api'
import { onMounted, ref } from 'vue'

const updateState = async (id, state) => {
  await api.changeState(id, state)
  const deletedIndex = tweets.value.findIndex(tweet => String(tweet.id) === id)
  tweets.value.splice(deletedIndex, 1)
}

const accepted = ref(0)
const declined = ref(0)
const initial = ref(0)

const tweets = ref([])

const breakpoint = 0.5
const INTERVAL = 60000

onMounted(async () => {
  await updateTweets()
})

const updateTweets = async () => {
  const output = await api.getStatistics()
  console.log(output)

  accepted.value = output.accepted
  declined.value = output.declined
  initial.value = output.initial

  tweets.value.push(await api.getLatestTweets())

  setTimeout(updateTweets, INTERVAL)
}
</script>

<style lang="sass" scoped>
.bad-progress
  :deep(.q-linear-progress__model--determinate)
    background: #EA0000

.good-progress
  :deep(.q-linear-progress__model--determinate)
    background: #06750A

.page-wrapper
  background: #F8F9FF

:deep(.twitter-tweet)
  margin: 0 !important

.button
  width: 48%
  border-radius: 8px
  text-transform: none
  font-weight: 600

.button-acccept
  background: #E8FFD2
  color: #06756E

.button-reject
  background: #FFEDF7
  color: #FF0000

.good-alert
  background: #D0FFB9
  color: #06756E
  font-size: 12px
  font-weight: 700

.bad-alert
  color: #FF0000
  background: #FFE7F4
  font-size: 12px
  font-weight: 700
</style>
