import React, { useState, useEffect } from 'react';
import { StyleSheet, View, Text, TextInput, Button, ActivityIndicator } from 'react-native';
import { saveTokens, getTokens, clearTokens } from '../storage/storage';
import { LOGIN_V1 } from '@/constant';
import { useRouter } from 'expo-router';

export default function LoginScreen() {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [accessToken, setAccessToken] = useState<string | null>(null);
    const [refreshToken, setRefreshToken] = useState<string | null>(null);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const loadTokens = async () => {
            const { accessToken, refreshToken } = await getTokens();
            if (accessToken && refreshToken) {
                setAccessToken(accessToken);
                setRefreshToken(refreshToken);
            }
        };
        loadTokens();
    }, []);

    const handleLogin = async () => {
        setLoading(true);
        setErrorMessage(null);

        try {
            const response = await fetch(`${LOGIN_V1}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
                    password,
                }),
            });

            const data = await response.json();

            if (response.ok && data?.data?.access_token && data?.data?.refresh_token) {
                await saveTokens(data.data.access_token, data.data.refresh_token);
                setAccessToken(data.data.access_token);
                setRefreshToken(data.data.refresh_token);
                router.push('/layout');
            } else {
                throw new Error(data?.message || 'Login failed');
            }
        } catch (error: any) {
            //console.error('Login error:', error);
            setErrorMessage(error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = async () => {
        await clearTokens();
        setAccessToken(null);
        setRefreshToken(null);
        setEmail('');
        setPassword('');
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Iniciar Sesión</Text>

            {errorMessage && <Text style={styles.error}>{errorMessage}</Text>}

            {!accessToken ? (
                <>
                    <TextInput
                        style={styles.input}
                        placeholder="Correo electrónico"
                        keyboardType="email-address"
                        value={email}
                        onChangeText={setEmail}
                        autoCapitalize="none"
                    />
                    <TextInput
                        style={styles.input}
                        placeholder="Contraseña"
                        secureTextEntry={true}
                        value={password}
                        onChangeText={setPassword}
                    />

                    {loading ? (
                        <ActivityIndicator size="large" />
                    ) : (
                        <Button title="Iniciar sesión" onPress={handleLogin} />
                    )}
                </>
            ) : (
                <View>
                    <Text style={styles.success}>¡Inicio de sesión exitoso!</Text>
                    <Text>Access Token: {accessToken.slice(0, 20)}...</Text>
                    <Text>Refresh Token: {refreshToken?.slice(0, 20)}...</Text>
                    <Button title="Cerrar sesión" onPress={handleLogout} />
                </View>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        paddingHorizontal: 20,
    },
    title: {
        fontSize: 24,
        marginBottom: 30,
        textAlign: 'center',
    },
    input: {
        height: 40,
        borderColor: 'gray',
        borderWidth: 1,
        marginBottom: 15,
        paddingHorizontal: 10,
    },
    error: {
        color: 'red',
        marginBottom: 10,
        textAlign: 'center',
    },
    success: {
        color: 'green',
        marginBottom: 10,
        fontWeight: 'bold',
        textAlign: 'center',
    },
});
