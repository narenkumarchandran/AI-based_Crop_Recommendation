import React from 'react';
import { View, Text, FlatList, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function MarketPricesScreen({ navigation }) {
  // Dummy data representing parsed Agmarknet XML payload
  const mockPrices = [
    { id: '1', commodity: 'Rice', variety: 'Common', modal_price: '₹2,500/q', market: 'Villupuram Market' },
    { id: '2', commodity: 'Maize', variety: 'Hybrid', modal_price: '₹1,900/q', market: 'Salem Market' },
    { id: '3', commodity: 'Cotton', variety: 'MCU-5', modal_price: '₹7,100/q', market: 'Erode Market' },
  ];

  const renderItem = ({ item }) => (
    <View className="bg-white p-4 rounded-2xl shadow-sm mb-4 border border-gray-100">
      <View className="flex-row justify-between mb-2">
        <Text className="text-xl font-bold text-dark">{item.commodity}</Text>
        <Text className="text-xl font-bold text-blue-600">{item.modal_price}</Text>
      </View>
      <View className="flex-row justify-between items-center text-gray-500">
        <Text className="text-sm font-medium">Variety: {item.variety}</Text>
        <Text className="text-xs bg-gray-100 px-2 py-1 rounded-md">{item.market}</Text>
      </View>
    </View>
  );

  return (
    <SafeAreaView className="flex-1 bg-gray-50">
      <View className="p-4 flex-row items-center justify-between">
        <Text className="text-2xl font-bold text-dark">Local Commodity Prices</Text>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text className="text-blue-500 font-medium">Close</Text>
        </TouchableOpacity>
      </View>
      <FlatList
        className="px-4 pt-2"
        data={mockPrices}
        keyExtractor={item => item.id}
        renderItem={renderItem}
        showsVerticalScrollIndicator={false}
      />
    </SafeAreaView>
  );
}
