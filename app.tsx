import React, { useEffect, useState } from 'react';
import { StyleSheet, View, Text, FlatList, ActivityIndicator } from 'react-native';
import axios from 'axios';
import { BarChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';

const App = () => {
  const [заявки, setЗаявки] = useState([]);
  const [график, setГрафик] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const заявкиResponse = await axios.get('http://127.0.0.1:5000/заявки');  // Замените на ваш IP и порт
      console.log('Заявки:', заявкиResponse.data);  // Отладка
      const графикResponse = await axios.get('http://127.0.0.1:5000/график_работы');  // Замените на ваш IP и порт
      console.log('График работы:', графикResponse.data);  // Отладка
      setЗаявки(заявкиResponse.data);
      setГрафик(графикResponse.data);
      setLoading(false);
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Заявки</Text>
      <FlatList
        data={заявки}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.item}>
            <Text>Заявка {item.id}</Text>
            <Text>Статус: {item.Статус}</Text>
            <Text>Стоимость: {item.Стоимость}</Text>
          </View>
        )}
      />
      <Text style={styles.title}>График работы</Text>
      <BarChart
        data={{
          labels: график.map((item) => item.Сотрудник),
          datasets: [
            {
              data: график.map((item) => item.Тип_времени === 'Полный рабочий день' ? 8 : 4)
            }
          ]
        }}
        width={Dimensions.get('window').width - 16}
        height={220}
        chartConfig={{
          backgroundColor: '#e26a00',
          backgroundGradientFrom: '#fb8c00',
          backgroundGradientTo: '#ffa726',
          decimalPlaces: 2,
          color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
          style: {
            borderRadius: 16
          }
        }}
        style={{
          marginVertical: 8,
          borderRadius: 16
        }}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 8,
  },
  title: {
    fontSize: 24,
    marginBottom: 16,
  },
  item: {
    marginBottom: 16,
  },
});

export default App;
