import React from 'react'
import { Button, Form, Input, Card, Divider, InputNumber, message } from 'antd';
import { useNavigate } from 'react-router-dom';


function CredentialsForm() {
    const navigate = useNavigate();
    const [messageApi, contextHolder] = message.useMessage();
    const [form] = Form.useForm();

    const onFinish = async (values) => {
        const res = await fetch("http://127.0.0.1:5000/sendCrentials",
            {
                method: "POST",
                body: JSON.stringify(values),
            });
        const data = await res.json();
        if (data.error) {
            messageApi.open({
                type: 'error',
                content: data.error
            })
        } else {
            navigate("/results");
        }
    };



    return (
        <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100%", width: "100%", backgroundColor: "rgb(244 244 245)" }} className='font-semibold'>
            {contextHolder}
            <Card
                title="Data profiler"
                bordered={false}
                className='font-semibold text-center p-4'
            >
                <Form
                    name="basic"
                    form={form}
                    onFinish={onFinish}
                    autoComplete="off"
                >
                    <Form.Item
                        label="Enter host:"
                        name="host"
                        rules={[
                            {
                                required: true,
                                message: 'Please enter host!',
                            },
                        ]}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        label="Enter port:"
                        name="port"
                        rules={[
                            {
                                required: true,
                                message: 'Please enter port!',
                            },
                        ]}
                    >
                        <InputNumber style={{ width: "100%" }} />
                    </Form.Item>
                    <Form.Item
                        label="Enter database name:"
                        name="dbName"
                        rules={[
                            {
                                required: true,
                                message: 'Please enter database name!',
                            },
                        ]}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        label="Enter username:"
                        name="username"
                        rules={[
                            {
                                required: true,
                                message: 'Please enter username!',
                            },
                        ]}
                    >
                        <Input />
                    </Form.Item>

                    <Form.Item
                        label="Password"
                        name="password"
                        rules={[
                            {
                                required: true,
                                message: 'Please input your password!',
                            },
                        ]}
                    >
                        <Input.Password />
                    </Form.Item>

                    <Divider />

                    <Form.Item
                        label="Enter config file:"
                        name="configFile"
                    >
                        <Input placeholder="Optional" />
                    </Form.Item>

                    <Form.Item

                    >
                        <Button type="primary" htmlType="submit" className='bg-blue-500 font-semibold py-5 px-8'>
                            Submit
                        </Button>
                    </Form.Item>
                </Form>
            </Card>
        </div>
    )
}

export default CredentialsForm