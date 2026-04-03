import React from 'react';
import { View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function DashboardScreen({ navigation }) {
  return (
    <SafeAreaView className="flex-1 bg-gray-50">
      <ScrollView className="flex-1 px-4 pt-4">
        <View className="mb-8">
          <Text className="text-sm font-medium text-gray-500 uppercase">Tuesday, Oct 24</Text>
          <Text className="text-3xl font-bold text-dark">Good Morning, Arun!</Text>
        </View>

        {/* Weather Widget */}
        <View className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 mb-6">
          <Text className="text-lg font-semibold text-gray-800 mb-2">Weather Forecast ⛅</Text>
          <View className="flex-row justify-between items-center mt-2">
            <View>
              <Text className="text-4xl font-bold text-dark">28°C</Text>
              <Text className="text-gray-500">Kanchipuram, TN</Text>
            </View>
            <View className="items-end">
              <Text className="text-blue-500 font-medium">Humidity: 65%</Text>
              <Text className="text-gray-400">Rain: 0mm</Text>
            </View>
          </View>
        </View>

        {/* Action Grid */}
        <View className="flex-row flex-wrap justify-between mb-6">
          <TouchableOpacity 
            className="w-[48%] bg-green-50 p-4 rounded-2xl mb-4 border border-green-100 h-32 justify-between"
            onPress={() => navigation.navigate('CropRecommendation')}
          >
            <Text className="text-3xl">🌱</Text>
            <Text className="font-semibold text-secondary">Crop AI Engine</Text>
          </TouchableOpacity>

          <TouchableOpacity 
            className="w-[48%] bg-blue-50 p-4 rounded-2xl mb-4 border border-blue-100 h-32 justify-between"
            onPress={() => navigation.navigate('MarketPrices')}
          >
            <Text className="text-3xl">📈</Text>
            <Text className="font-semibold text-blue-700">Market Prices</Text>
          </TouchableOpacity>

          <TouchableOpacity 
            className="w-full bg-purple-50 p-4 rounded-2xl mb-4 border border-purple-100 h-32 justify-between flex-row items-end"
            onPress={() => navigation.navigate('Chatbot')}
          >
            <View>
              <Text className="text-3xl mb-2">🤖</Text>
              <Text className="font-semibold text-purple-700">Agri Advisor Gemini</Text>
            </View>
            <Text className="text-purple-500 font-medium text-sm pb-1">Ask anything →</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
