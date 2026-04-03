import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity } from 'react-native';

export default function AuthScreen({ navigation }) {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <View className="flex-1 justify-center bg-white px-6">
      <View className="mb-10">
        <Text className="text-4xl font-extrabold text-dark tracking-tight mb-2">
          {isLogin ? 'Welcome Back' : 'Create Account'}
        </Text>
        <Text className="text-gray-500 text-lg">
          {isLogin ? 'Login to continue to your dashboard' : 'Join the farming revolution'}
        </Text>
      </View>

      <TextInput 
        className="w-full bg-gray-50 border border-gray-200 rounded-xl p-4 mb-4 text-dark text-lg"
        placeholder="Username"
        placeholderTextColor="#9ca3af"
      />
      <TextInput 
        className="w-full bg-gray-50 border border-gray-200 rounded-xl p-4 mb-8 text-dark text-lg"
        placeholder="Password"
        secureTextEntry
        placeholderTextColor="#9ca3af"
      />

      <TouchableOpacity 
        className="bg-primary w-full py-4 rounded-xl mb-6 shadow-md"
        onPress={() => navigation.replace('Dashboard')}
      >
        <Text className="text-white text-center font-bold text-lg tracking-wide">
          {isLogin ? 'Login' : 'Sign Up'}
        </Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={() => setIsLogin(!isLogin)} className="py-2">
        <Text className="text-secondary text-center font-semibold text-base">
          {isLogin ? "Don't have an account? Sign Up" : "Already have an account? Login"}
        </Text>
      </TouchableOpacity>
    </View>
  );
}
