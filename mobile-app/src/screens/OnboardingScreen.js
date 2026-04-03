import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';

export default function OnboardingScreen({ navigation }) {
  return (
    <View className="flex-1 items-center justify-center bg-white px-6">
      <Text className="text-3xl font-bold text-primary mb-6">Farmer's Friend</Text>
      <Text className="text-center text-gray-600 mb-12 text-lg leading-relaxed">
        Your AI-driven agricultural assistant for localized insights, recommendations, and market data.
      </Text>
      
      <Text className="text-gray-500 mb-4 font-medium uppercase tracking-widest">Select Language</Text>
      
      <TouchableOpacity 
        className="bg-primary w-full py-4 rounded-xl mb-4 shadow-sm"
        onPress={() => navigation.navigate('Auth')}
      >
        <Text className="text-white text-center font-semibold text-lg">English</Text>
      </TouchableOpacity>
      
      <TouchableOpacity 
        className="bg-green-100 w-full py-4 rounded-xl mb-4 border border-green-200"
        onPress={() => navigation.navigate('Auth')}
      >
        <Text className="text-secondary text-center font-semibold text-lg">हिंदी</Text>
      </TouchableOpacity>
      
      <TouchableOpacity 
        className="bg-green-100 w-full py-4 rounded-xl border border-green-200"
        onPress={() => navigation.navigate('Auth')}
      >
        <Text className="text-secondary text-center font-semibold text-lg">தமிழ்</Text>
      </TouchableOpacity>
    </View>
  );
}
