import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function CropRecommendationScreen() {
  const [form, setForm] = useState({
    N: '', P: '', K: '', temperature: '', humidity: '', ph: '', rainfall: ''
  });
  const [result, setResult] = useState(null);

  const autoFillIoT = () => {
    // Simulated IoT sync
    setForm({ N: '90', P: '42', K: '43', temperature: '28', humidity: '65', ph: '6.5', rainfall: '200' });
  };

  const predictCrop = () => {
    // Simulated API call latency
    setTimeout(() => setResult({ recommendation: 'rice' }), 500);
  };

  return (
    <SafeAreaView className="flex-1 bg-white">
      <ScrollView className="px-4 pt-4">
        <Text className="text-2xl font-bold text-dark mb-4">Crop AI Engine</Text>
        
        <TouchableOpacity 
          className="bg-secondary p-4 rounded-xl mb-6 flex-row items-center justify-center"
          onPress={autoFillIoT}
        >
          <Text className="text-white font-semibold mr-2">Sync with ESP32 Sensors</Text>
          <Text className="text-white opacity-75 text-xs">(Premium)</Text>
        </TouchableOpacity>

        <View className="flex-row flex-wrap justify-between">
          <View className="w-[48%] mb-4">
            <Text className="text-gray-500 mb-1 text-xs">Nitrogen (N)</Text>
            <TextInput className="bg-gray-50 border border-gray-200 p-3 rounded-lg" keyboardType="numeric" value={form.N} onChangeText={t => setForm({...form, N: t})} />
          </View>
          <View className="w-[48%] mb-4">
            <Text className="text-gray-500 mb-1 text-xs">Phosphorus (P)</Text>
            <TextInput className="bg-gray-50 border border-gray-200 p-3 rounded-lg" keyboardType="numeric" value={form.P} onChangeText={t => setForm({...form, P: t})} />
          </View>
          {/* Omit other inputs for brevity in this boilerplate, they follow the same pattern */}
          <View className="w-full mb-4">
            <Text className="text-gray-500 mb-1 text-xs">Potassium (K)</Text>
            <TextInput className="bg-gray-50 border border-gray-200 p-3 rounded-lg" keyboardType="numeric" value={form.K} onChangeText={t => setForm({...form, K: t})} />
          </View>
        </View>

        <TouchableOpacity className="bg-primary p-4 rounded-xl mt-4 shadow-md" onPress={predictCrop}>
          <Text className="text-white text-center font-bold text-lg">Analyze Farm 🌱</Text>
        </TouchableOpacity>

        {result && (
          <View className="mt-8 bg-green-50 p-6 rounded-2xl items-center border border-green-200">
            <Text className="text-gray-600 mb-2 font-medium">Recommended Crop</Text>
            <Text className="text-4xl text-secondary font-bold uppercase tracking-widest">{result.recommendation}</Text>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}
