import React, { useEffect, useState } from 'react';
import { Spin } from "antd";
import { useNavigate } from 'react-router-dom';


const Results = () => {
    const navigate = useNavigate();
    const [filterInput, setFilterInput] = useState('');
    const [selectedTable, setSelectedTable] = useState('');
    const [tableAnalitics, setTableAnalitics] = useState([]);

    const [tables, setTables] = useState([]);
    const [filteredTables, setFilteredTables] = useState([]);

    useEffect(() => {
        const getTables = async () => {
            const res = await fetch("http://127.0.0.1:5000/getDBTables",
                {
                    method: "GET",
                });
            const data = await res.json();
            return data.tables;
        }
        getTables().then(tables => {
            if (tables.length === 0) {
                navigate("/");
            } else {
                setFilteredTables(tables);
                setTables(tables);
            }
        });
    }, [])

    useEffect(() => {
        let arr = tables.filter(table => table.includes(filterInput));
        setFilteredTables(arr);
    }, [filterInput]);

    useEffect(() => {
        const getTableAnalitics = async () => {
            const res = await fetch(`http://127.0.0.1:5000/getTableInfo/${selectedTable}`,
                {
                    method: "GET",
                });
            const data = await res.json();
            return data.result;
        }
        selectedTable && getTableAnalitics().then(data => setTableAnalitics(data));
        return () => {
            setTableAnalitics([]);
        }
    }, [selectedTable])

    const handleTableFilterChange = (e) => {
        setFilterInput(e.target.value);
    };

    return (
        <div className="flex h-[100vh]">
            <div className="w-1/4 bg-zinc-100 p-4 fixed top-0 left-0 h-[100%]">
                <h2 className="text-lg font-semibold mb-2">Database Tables</h2>
                <h2 className="text-m font-semibold mb-4">{filteredTables.length} tables</h2>
                <input
                    type="text"
                    placeholder="Filter Tables"
                    className="w-full p-2 mb-4 border rounded"
                    value={filterInput}
                    onChange={handleTableFilterChange}
                />
                <div className="space-y-2 h-[80vh] mb-1 overflow-scroll">
                    <button className="w-full p-2 bg-blue-900 text-white rounded" onClick={() => setSelectedTable('relations')}>Table relations</button>
                    {filteredTables.length === 0 ?
                        filterInput ? <h3 className="w-full pt-2">No results</h3> : <Spin className="w-full pt-6" tip="Loading" size="large"></Spin>
                        : (filteredTables.map(table => (
                            <button className="w-full p-2 bg-blue-500 text-white rounded" onClick={() => setSelectedTable(table)}>{table}</button>
                        )))
                    }
                </div>
            </div>

            <div className="w-3/4 p-4 ml-[25%]">
                <div className='flex flex-row justify-between items-start py-2'>
                    <h1 className="text-3xl font-semibold mb-4">{selectedTable ? `Table ${selectedTable}` : 'Select option from left-hand side'}</h1>
                    <button className="w-16 p-2 bg-blue-900 text-white rounded" onClick={() => navigate("/")}>Exit</button>
                </div>
                {tableAnalitics.length > 0 ? (
                    <>
                        {selectedTable !== 'relations' && (
                            <div className="grid grid-cols-2 gap-4 mb-4">
                                <div className="p-4 bg-white shadow rounded">
                                    <h2 className="text-lg font-semibold">Number of rows</h2>
                                    <p className="text-2xl">{tableAnalitics.find(el => el.label === 'RowNum')?.value}</p>
                                </div>
                                <div className="p-4 bg-white shadow rounded">
                                    <h2 className="text-lg font-semibold">Number of columns</h2>
                                    <p className="text-2xl">{tableAnalitics.find(el => el.label === 'ColNum')?.value}</p>
                                </div>
                            </div>
                        )}
                        <div className="mb-4 min-h-[50%]">
                            <h2 className="text-2xl font-semibold mb-2">Results</h2>
                            <div className="bg-white shadow rounded p-4 h-[100%]">
                                {tableAnalitics.filter(el => !['ColNum', 'RowNum'].includes(el.label)).map(analytic => (
                                    <div className="mb-4">
                                        <h2 className="text-m font-semibold mb-2">{analytic.label}</h2>
                                        <div className="bg-white shadow rounded p-4 h-[100%]">
                                            {analytic.valueIsArr ? (
                                                analytic.value.map(value => {
                                                    if (typeof value === 'object')
                                                        return (<><p>{value.label}</p>
                                                            {value.value.map(el => <p className='pl-5'>{el}</p>)}
                                                        </>)
                                                    else return <p>{value}</p>
                                                })
                                            ) : (
                                                <p>{analytic.value}</p>
                                            )}
                                        </div>
                                    </div>
                                ))
                                }
                            </div>
                        </div>

                    </>
                ) : selectedTable && <Spin className="w-full min-h-full pt-10 grid justify-center items-center" tip="Loading" size="large"></Spin>}
            </div>
        </div>
    );
};

export default Results;
